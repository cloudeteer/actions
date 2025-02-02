from unittest.mock import patch, mock_open
from main import get_required_version


# Test case: Valid Terraform file with required_version
def test_get_required_version_valid(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")

    tf_content = """
    terraform {
      required_version = ">= 1.9"
    }
    """
    with patch("builtins.open", mock_open(read_data=tf_content)):
        with patch("glob.glob", return_value=["/mock/directory/valid.tf"]):
            result = get_required_version()
            assert result == ">= 1.9", "Should correctly parse required_version."


# Test case: Valid Terraform file with required_version (Regressiontest for https://github.com/cloudeteer/actions/issues/4)
def test_get_required_version_with_multiline_condition(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")

    tf_content = """
    terraform {
      required_version = "1.0"
    }

    variable "debug" {
      validation {
        condition     = (false && !false)
        || (!false && false)
        || (!false && !false)
        error_message = "Debug"
      }
    }
    """
    with patch("builtins.open", mock_open(read_data=tf_content)):
        with patch("glob.glob", return_value=["/mock/directory/valid.tf"]):
            result = get_required_version()
            assert result == "1.0", "Should correctly parse required_version."


# Test case: Multiple Terraform files, one with required_version
def test_get_required_version_multiple_files(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")

    tf_content_1 = """
    terraform {
      required_version = ">= 1.0"
    }
    """
    tf_content_2 = """
    terraform {
      required_version = ">= 1.9"
    }
    """
    # Mock the files and directory structure
    with patch("builtins.open", side_effect=[mock_open(read_data=tf_content_1).return_value, mock_open(read_data=tf_content_2).return_value]):
        with patch("glob.glob", return_value=["/mock/directory/valid1.tf", "/mock/directory/valid2.tf"]):
            result = get_required_version()
            assert result == ">= 1.9", "Should return the correct required_version from the files."

def test_get_required_version_not_found(monkeypatch):
    # Mock environment variable
    monkeypatch.setenv("directory", "/mock/directory")

    tf_content = """
    terraform {}
    """
    with patch("builtins.open", mock_open(read_data=tf_content)):
        version = get_required_version()
        assert version is None, "If no required_version is found, the return value should be None."

# Test case: No .tf files in the directory
def test_get_required_version_no_tf_files(monkeypatch):
    monkeypatch.setenv("directory", "/empty/directory")

    with patch("glob.glob", return_value=[]):
        version = get_required_version()
        assert version is None, "If no required_version is found, the return value should be None."

# Test case: Directory with empty Terraform files
def test_get_required_version_empty_tf_files(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")

    tf_content = ""  # Empty Terraform file
    with patch("builtins.open", mock_open(read_data=tf_content)):
        with patch("glob.glob", return_value=["/mock/directory/empty.tf"]):
            version = get_required_version()
            assert version is None, "If no required_version is found, the return value should be None."

# Test case: Valid Terraform file with required_version and commented versions
def test_get_required_version_commented_versions(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")

    tf_content = """
    terraform {
      #required_version = ">= 1.7"
      required_version = ">= 1.9"
      #required_version = ">= 1.10"
    }
    """
    with patch("builtins.open", mock_open(read_data=tf_content)):
        with patch("glob.glob", return_value=["/mock/directory/valid.tf"]):
            result = get_required_version()
            assert result == ">= 1.9", "Should correctly parse required_version."

# Test case: Valid .terraform-version file
def test_terraform_version_from_terraform_version_file(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")
    monkeypatch.setenv("file", ".terraform-version")
    monkeypatch.setenv("pattern", r'^(.*)$')

    tf_content = "1.9"
    with patch("builtins.open", mock_open(read_data=tf_content)):
        with patch("glob.glob", return_value=["/mock/directory/.terraform-version"]):
            result = get_required_version()
            assert result == "1.9", "Should correctly parse required_version."

# Test case: Valid .tools-version (asdf) file
def test_terraform_version_from_asdf_file(monkeypatch):
    monkeypatch.setenv("directory", "/mock/directory")
    # see: https://asdf-vm.com/manage/configuration.html
    monkeypatch.setenv("file", ".tool-versions")
    monkeypatch.setenv("pattern", r'^terraform (.*)$')

    tf_content = """
    ruby 2.5.3 # This is a comment
    terraform 1.9
    # This is another comment
    nodejs 10.15.0
    """
    # trim content
    tf_content = "\n".join([line.strip() for line in tf_content.split("\n")])
    with patch("builtins.open", mock_open(read_data=tf_content)):
        with patch("glob.glob", return_value=["/mock/directory/.tool-versions"]):
            result = get_required_version()
            assert result == "1.9", "Should correctly parse required_version."
