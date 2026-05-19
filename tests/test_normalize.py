import re
from urllib.parse import unquote_plus

# --- functions under test ---

def normalize_name(value):
    decoded_value = unquote_plus(str(value))
    return re.sub(r"\s+", " ", decoded_value).strip().casefold()


def normalize_region_name(value):
    normalized = normalize_name(value)
    return re.sub(r"\s+region$", "", normalized).strip()


# --- normalize_name ---

class TestNormalizeName:

    # URL decoding
    def test_decodes_percent_encoded_spaces(self):
        assert normalize_name("Dar%20es%20Salaam") == "dar es salaam"

    def test_decodes_plus_encoded_spaces(self):
        assert normalize_name("Dar+es+Salaam") == "dar es salaam"

    def test_decodes_mixed_encoding(self):
        assert normalize_name("Dar%20es+Salaam") == "dar es salaam"

    def test_decodes_percent_encoded_special_chars(self):
        assert normalize_name("Cote%20d%27Ivoire") == "cote d'ivoire"

    # Whitespace normalisation
    def test_collapses_multiple_spaces(self):
        assert normalize_name("Dar  es   Salaam") == "dar es salaam"

    def test_collapses_tabs_and_newlines(self):
        assert normalize_name("Dar\tes\nSalaam") == "dar es salaam"

    def test_strips_leading_and_trailing_whitespace(self):
        assert normalize_name("  Dar es Salaam  ") == "dar es salaam"

    # Case folding
    def test_lowercases_ascii(self):
        assert normalize_name("DAR ES SALAAM") == "dar es salaam"

    def test_casefolds_unicode(self):
        # ß should casefold to ss, not just lowercase to ß
        assert normalize_name("Straße") == "strasse"

    # Type coercion
    def test_accepts_integer(self):
        assert normalize_name(123) == "123"

    def test_accepts_none_as_string(self):
        assert normalize_name(None) == "none"

    # Already clean input
    def test_already_normalised_value_is_unchanged(self):
        assert normalize_name("dar es salaam") == "dar es salaam"

    def test_empty_string(self):
        assert normalize_name("") == ""


# --- normalize_region_name ---

class TestNormalizeRegionName:

    # Core Dar es Salaam cases
    def test_strips_region_suffix(self):
        assert normalize_region_name("Dar es Salaam Region") == "dar es salaam"

    def test_strips_region_suffix_case_insensitive(self):
        assert normalize_region_name("Dar es Salaam REGION") == "dar es salaam"

    def test_strips_region_suffix_with_extra_space(self):
        assert normalize_region_name("Dar es Salaam  Region") == "dar es salaam"

    def test_decodes_url_encoding_then_strips_suffix(self):
        assert normalize_region_name("Dar%20es%20Salaam%20Region") == "dar es salaam"

    def test_decodes_plus_encoding_then_strips_suffix(self):
        assert normalize_region_name("Dar+es+Salaam+Region") == "dar es salaam"

    # Other regions
    def test_strips_suffix_from_other_regions(self):
        assert normalize_region_name("Arusha Region") == "arusha"

    def test_strips_suffix_from_mwanza(self):
        assert normalize_region_name("Mwanza Region") == "mwanza"

    # Should NOT strip mid-string "region"
    def test_does_not_strip_region_in_middle_of_name(self):
        assert normalize_region_name("Lake Region District") == "lake region district"

    # No suffix present
    def test_name_without_suffix_is_unchanged(self):
        assert normalize_region_name("Dodoma") == "dodoma"

    # Edge cases
    def test_empty_string(self):
        assert normalize_region_name("") == ""

    def test_only_region_word_is_kept(self):
        # regex requires whitespace BEFORE "region", so a bare "Region" is not stripped
        assert normalize_region_name("Region") == "region"

    def test_already_normalised_value_is_unchanged(self):
        assert normalize_region_name("dar es salaam") == "dar es salaam"