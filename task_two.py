import pandas as pd
import tabula

if __name__ == "__main__":

    # (After running task_one) reading archive pdf:
    file = 'output/Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536_RN537.pdf'

    tables = tabula.read_pdf(file, pages = 'all', multiple_tables = True)

    df_final = pd.concat(tables) # grouping all tables in only one

    # pre-processing, change legends and cleaning data like NaN:
    df_final['OD'].replace({"OD":"Seg. Odontológica"}, inplace = True)
    df_final['AMB'].replace({"AMB":"Seg. Ambulatorial"}, inplace = True)
    df_final.fillna(value = "")

    # saving as .csv file
    df_final.to_csv('AnexoI.csv', index=False)

    # compressin file
    compression_opts = dict(method='zip',
                            archive_name='AnexoI.csv')
    df_final.to_csv('Teste_{AndrePavan}.zip', index=False, compression=compression_opts)

