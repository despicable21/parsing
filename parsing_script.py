import os 
from bitcoinlib.transactions import Transaction 

def parse_transactions_from_file(file_path, output_file):

    with open(file_path, 'r') as file:
        raw_txs = file.read().strip().split('\n\n') #удаляем пробелы в начале и конце, разделяем на отдельные строки
    
    
    parsed_txs = [] #пустой список для хранения данных разобранных транзакций

    with open(output_file, 'w', encoding='utf-8') as out_f:
        
        for raw_tx in raw_txs: #перебираем каждую сырую транзакцию
            try:
                #чистим от пробелов и переносов строк, чтобы получить непрерывную hex-строку
                raw_tx = raw_tx.strip().replace('\n', '')
                
                #пропускаем пустые строки
                if not raw_tx:
                    continue
                
                tx = Transaction.parse(raw_tx, network='bitcoin') #парсим hex-строку в объект Transaction
                
                #словарь для хранения ключевых данных транзакции
                tx_data = {
                    'txid': tx.txid,  #хэш
                    'version': tx.version,  #версия протокола транзакции
                    'locktime': tx.locktime,  #время блокировки (если 0, транзакция может быть включена в блокчейн немедленно)
                    'inputs': [],  #хранение данных о входах
                    'outputs': []  #хранение данных о выходах
                }
                
                #парсим и добавляем данные о каждом входе
                for inp in tx.inputs:
                    tx_data['inputs'].append({
                        'prev_txid': inp.prev_txid.hex(),  #хэш предыдущей транзакции
                        'output_n': inp.output_n,  #индекс выхода из предыдущей транзакции
                        'script': inp.script.serialize().hex(),  #сериализованный hex-код ScriptSig
                    })
                
                #парсим и добавляем данные о каждом выходе
                for out in tx.outputs:
                    tx_data['outputs'].append({
                        'value_satoshi': out.value,  #сумма в сатоши (1 BTC = 100,000,000 сатоши)
                        'address': out.address or 'N/A',  #адрес Bitcoin, если его можно вывести
                        'script_type': out.script_type,  #тип скрипта
                        'script': out.script.serialize().hex()  #сериализованный hex-код ScriptPubKey
                    })
                
                
                parsed_txs.append(tx_data) #добавляем разобранные данные транзакции в список
                
                #записываем данные в выходной файл.
                out_f.write(f"\nИдентификатор транзакции: {tx_data['txid']}\n")
                out_f.write(f"Версия: {tx_data['version']}\n")
                out_f.write(f"Время блокировки: {tx_data['locktime']}\n")
                out_f.write("\nВходы:\n")
                for i, inp in enumerate(tx_data['inputs']):
                    out_f.write(f"  Вход {i}:\n")
                    out_f.write(f"    Хэш предыдущей транзакции: {inp['prev_txid']}\n")
                    out_f.write(f"    Индекс выхода: {inp['output_n']}\n")
                    out_f.write(f"    Скрипт: {inp['script']}\n")
                out_f.write("\nВыходы:\n")
                for i, out in enumerate(tx_data['outputs']):
                    out_f.write(f"  Выход {i}:\n")
                    out_f.write(f"    Сумма: {out['value_satoshi']} сатоши ({out['value_satoshi'] / 100000000:.8f} BTC)\n")
                    out_f.write(f"    Адрес: {out['address']}\n")
                    out_f.write(f"    Тип скрипта: {out['script_type']}\n")
                    out_f.write(f"    Скрипт: {out['script']}\n")
                
            except Exception as e:
                out_f.write(f"Ошибка при парсинге транзакции {raw_tx[:20]}...: {str(e)}\n")
    
    
    return parsed_txs #возвращаем список транзакций

def main():

    input_file = 'txs_raw.txt'
    output_file = 'output.txt'

    if not os.path.exists(input_file):
        print(f"Ошибка: Файл {input_file} не найден.")
        return
    

    parsed_txs = parse_transactions_from_file(input_file, output_file)
    


if __name__ == "__main__":
    main()