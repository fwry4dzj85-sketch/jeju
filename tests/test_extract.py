from tpwa.extract import clean_text, is_valid_sentence, remove_references, split_sentences


def test_remove_references_section():
    text = "This is body text.\nReferences\n[1] A paper."
    assert remove_references(text).strip() == "This is body text."


def test_clean_text_removes_citation_and_formula_like_text():
    text = "It follows that S=A/4G. This result is important [15].\nReferences\n[1] ignored"
    cleaned = clean_text(text)
    assert "[15]" not in cleaned
    assert "References" not in cleaned


def test_split_sentences_keeps_common_abbreviations():
    sentences = split_sentences("See Ref. for details. We now turn to the proof.")
    assert sentences == ["See Ref. for details.", "We now turn to the proof."]


def test_sentence_filtering():
    assert not is_valid_sentence("Yes.")
    assert is_valid_sentence("We now turn to the proof of the main theorem.")
