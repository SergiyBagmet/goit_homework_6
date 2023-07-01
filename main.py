from pathlib import Path
import sys

arg = sys.argv[1] # название папки для сортировки (рабочий стол/dir)
path = Path.home() / "Desktop" / arg 
main_path = path # путь к нашей папке для создания нових

# известние файли для сортировки
FILE_EXTENSIONS = {
    'images': {'.jpeg', '.png', '.jpg', '.svg'},
    'video': {'.avi', '.mp4', '.mov', '.mkv'},
    'documents': {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'},
    'audio': {'.mp3', '.ogg', '.wav', '.amr'},
    'archives': {'.zip', '.gz', '.tar'}
}



# константи для переименования файлов
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c,t in zip(CYRILLIC_SYMBOLS,TRANSLATION):

    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()



def normalize(name : str) -> str :
    """
    транлитерация кирилици
    замена всего кроме латинского алфавита и чисел на _
    """
    if name.isalnum() :              
        return name.translate(TRANS)
    else:
        new_name = ""
        for ch in name:           
            if ch.isalnum():
                new_name += ch.translate(TRANS)
            else :
                new_name += "_"    
        return new_name


  



def directory_tree (path: Path) :
    """
    основной рекурсивний проход 
    всех папок и файлов
    """
    for item in path.iterdir() :
        if item.is_file():
            
            new_name = normalize(str(item.stem)) + str(item.suffix) # новое имя + суфикс
            item = item.rename(item.parent / new_name) # переименование файлов + присваеваем новий путь

            name_dir = "" # получаем имя для новой папки соответствующей файловой группе 
            for key,val in FILE_EXTENSIONS.items():
                if item.suffix in val : #
                    name_dir = key
                    break
            if not name_dir: # если нет совпадений по константе
                name_dir = "others"    
            
            new_dir_path = main_path / name_dir # путь к новой папке для ее создание и переноса файлов
            new_dir_path.mkdir(exist_ok=True) # создаем новую папку если такой нет 
            # перенос файлов 


            #заполнение словаря-> категория : [файли]
            if name_dir not in my_dict_files : # если нет ключа создаем ключ:спиок
                my_dict_files[name_dir] = [item.name]
               

            else:
                my_dict_files[name_dir].append(item.name)     
            
            


        elif item.is_dir():
            directory_tree(path / item.name)



if __name__ == "__main__" :

    # получаем сет всех известих расширений из константного словаря
    all_extens = set()
    for ext in FILE_EXTENSIONS.values():
        all_extens.update(ext)

    my_dict_files = {} # словарь список файлов по категориям

    directory_tree(path)
    
    

    