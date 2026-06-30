from tpwa.classify import RuleBasedClassifier, parse_classification


def test_transition_sentence():
    result = RuleBasedClassifier().classify("We now turn to the proof of the main theorem.")
    assert result.category == "Transition"


def test_derivation_sentence():
    result = RuleBasedClassifier().classify("It follows immediately that the entropy is proportional to the horizon area.")
    assert result.category == "Derivation"


def test_introduction_sentence():
    result = RuleBasedClassifier().classify("In this paper, we study conformal field theories on curved backgrounds.")
    assert result.category == "Introduction"


def test_parse_classification_bounds_confidence():
    result = parse_classification('{"category":"Derivation","confidence":2,"reason":"logical consequence"}')
    assert result.category == "Derivation"
    assert result.confidence == 1.0
