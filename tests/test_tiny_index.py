from tiny_index.index import Index


def test_search():
    index = Index(["肝炎", "肥大性肝炎", "日本脳炎"])
    results = index.search("肝炎")
    assert len(results) == 2
    assert results[0][0] == '肝炎'
    assert results[1][0] == '肥大性肝炎'


def test_yomi_search():
    index = Index(["肝炎", "肥大性肝炎", "日本脳炎"])
    results = index.search("かんえん")
    assert len(results) == 2
    assert results[0][0] == '肝炎'
    assert results[1][0] == '肥大性肝炎'

# Ref sample in https://github.com/builtinnya/fuzzlogia
def test_ginga():
    index = Index(['電気羊', '銀河ヒッチハイクガイド'])
    results = index.search('ぎんが')
    assert len(results) == 1
    assert results[0][0] == '銀河ヒッチハイクガイド'


# Ref sample in https://github.com/builtinnya/fuzzlogia
def test_ginga2():
    index = Index(['電気羊', '銀河ヒッチハイクガイド'])
    results = index.search('ヒッチハイク')
    assert len(results) == 1
    assert results[0][0] == '銀河ヒッチハイクガイド'