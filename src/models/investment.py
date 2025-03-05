def calculate_profit(miktar, alis_fiyati, current_fiyat):
    """Yatırımın karını hesaplar"""
    alis_tutari = miktar * alis_fiyati
    suan_deger = miktar * current_fiyat
    return suan_deger - alis_tutari
