# this file is to enable the creation and consolidation of a dictionary that holds a primary and ensuing per-chunk dataframes
# for the purpose of statistical analysis of the evidence based, extracted information
# the dataframe will belong to a particular uploaded text/ run


# the generated per-chunk json files will be parsed here, cleaned and loaded into the dataframe


# dataframe has the following structure
# col 0 | col 1 | col 2 | col 3 |
# chunk |themes |chlngs.|exprncs|
# 1     |{Academic:eID, Challenging:eID} | [Stress:eID]| [CS Deadline:eID]


# note that eID == evidenceID, in notation x-XX | chunkSerialNumber | eID from chunk 7, extraction 13, would be 7-13


from chunk_parse import load_chunk_dataframe

OUTPUT_CSV = "extractions.csv"


def main():
    df = load_chunk_dataframe()
    if df.empty:
        print("No accepted extractions found.")
        return

    df.to_csv(OUTPUT_CSV, index=False)

    # print(f"{len(df)} extractions across {df['chunk_id'].nunique()} chunks -> {OUTPUT_CSV}")
    print(df.head)





if __name__ == "__main__":
    main()