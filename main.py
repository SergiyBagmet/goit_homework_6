from pathlib import Path
import shutil

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



def  extract_archive(archive_path: Path, del_archive=True) :
    """
    разархивируем архив в папку с именем архива
    с флагом на удаление архива + ловим ошибку
    """
    target_dir = archive_path.parent / archive_path.stem # путь для созданием папки с именем архива
    target_dir.mkdir(exist_ok=True) # создаем папку для архива
    try:
        shutil.unpack_archive(archive_path, target_dir) # распаковка
        if del_archive: # удаляем архив по флагу после распаковки
            archive_path.unlink()
    except ValueError:
        print(f"Не удалось разпаковать архив : {archive_path.name}")
  


def input_path()-> Path:
    """
    инпут пути к папке 
    проверка на валидность(существует+папка)
    """
    while True:
        path = Path(input("Введите полний путь к папке которую хотите отсортировать:\n"))
        if path.exists() and path.is_dir():
            return path
        else:
            print("введений вами путь не существует или не является папкой\n")            




def directory_tree (path: Path,  my_dict_files=None) :
    """
    основной рекурсивний проход 
    всех папок и файлов
    """
    for item in path.iterdir() :
        if item.is_file():
            
            new_name = normalize(item.stem) + item.suffix # новое имя + суфикс
            item = item.rename(item.parent / new_name) # переименование файлов + присваеваем новий путь

            name_dir = "" # получаем имя для новой папки соответствующей файловой группе 
            for key,val in FILE_EXTENSIONS.items():
                if item.suffix in val : #
                    name_dir = key
                    break
            if not name_dir: # если нет совпадений по константе
                name_dir = "others"    
            
            # заполнение сета расширений my_extens
            # + заполнение my_dict_files-> категория : [файли]
            my_extens.add(item.suffix)
            if  my_dict_files is None :  my_dict_files = {} #создаем словарь на первом заходе 
            if name_dir not in my_dict_files : # если нет ключа создаем ключ:спиок
                my_dict_files[name_dir] = [item.stem]
            else:
                my_dict_files[name_dir].append(item.stem)         

            # создание папок + перемещение файлов + работа с архивами 
            new_dir_path = main_path / name_dir # путь к новой папке для ее создание и переноса файлов
            new_dir_path.mkdir(exist_ok=True) # создаем новую папку если такой нет 
            item = item.replace(new_dir_path / item.name) # перенос файлов в папки по категориям

            if name_dir == "archives": # если категория ахиви(файл можно разпаковать) 
                extract_archive(item) # разпаковка + по умолчанию флаг на удаление 
            
            

        elif item.is_dir() and (item.name not in FILE_EXTENSIONS) : # проверка на папку и она не из наших ключей

            my_dict_files = directory_tree(path / item.name, my_dict_files) # рекурсивний заход + my_dict_files-> категория : [файли]
            
            if not any(item.iterdir()): # проверка на пустую папку
                item.rmdir()            # удаляем папку(пустую)

    return  my_dict_files



if __name__ == "__main__" :

    # получаем сет всех известих(скрипту) расширений из константного словаря
    all_extens = set()
    for ext in FILE_EXTENSIONS.values():
        all_extens.update(ext)

    # my_dict_files = {} # словарь для записи -  категория : [файли]
    my_extens = set() # сет для записи всех имеющихся расширений в папке

    path = input_path()
    main_path = path # путь к нашей папке для создания нових
    my_dict_files = directory_tree(path)
    

    
    print("\nсписок файлов в сортированной дериктории  по категориям :\n")
    for key, val in my_dict_files.items() :
        val_str = ", ".join(val)
        print("{:<10}: {}".format(key,val_str))
    
    print("\nПеречень всех известних расширений в сортированной директории :\n")
    know_extens = all_extens.intersection(my_extens)
    print("\t".join(know_extens))

    print("\nПеречень всех расширений не известних данному скрипту :\n")
    n_know_extens = my_extens.difference(know_extens)
    print("\t".join(n_know_extens))