def mergeTables(adx, time_s, b_bands):
    df = time_s.merge(b_bands, left_index = True, right_index = True, how = "inner")
    df = df.merge(adx,left_index = True, right_index = True, how = "inner" )
    return df

def binaryConvert(table):
    table["next_close"] = table["close"].shift(-1)
    table["target"] = (table["next_close"] > table["close"]).astype(int)

    #drop the last row since the shift 
    table = table.iloc[:-1]
    return table

