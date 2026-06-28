# Установка

```bash
pip install cai-framework
```

!!! tip "🚀 Ищете CAI PRO?"
    **CAI PRO** включает неограниченный доступ к нашей передовой модели `alias1`, терминальный интерфейс и профессиональную поддержку.
    **[Узнать больше о CAI PRO →](cai_pro.md)**

Ниже приведены подробные инструкции для популярных операционных систем. Для инструкций, связанных с разработкой, смотрите раздел [Development](cai_development.md).

### macOS
```bash
brew update && \
    brew install git python@3.12

# Создаём виртуальное окружение
python3.12 -m venv cai_env

# Устанавливаем пакет из локальной папки
source cai_env/bin/activate && pip install cai-framework

# Генерируем файл .env и заполняем значениями по умолчанию
echo -e 'OPENAI_API_KEY="sk-1234"\nANTHROPIC_API_KEY=""\nOLLAMA=""\nPROMPT_TOOLKIT_NO_CPR=1' > .env

# Запускаем CAI
cai  # первый запуск может занять до 30 секунд
```

### Ubuntu 24.04
```bash
sudo apt-get update && \
    sudo apt-get install -y git python3-pip python3.12-venv

# Создаём виртуальное окружение
python3.12 -m venv cai_env

# Устанавливаем пакет из локальной папки
source cai_env/bin/activate && pip install cai-framework

# Генерируем файл .env и заполняем значениями по умолчанию
echo -e 'OPENAI_API_KEY="sk-1234"\nANTHROPIC_API_KEY=""\nOLLAMA=""\nPROMPT_TOOLKIT_NO_CPR=1' > .env

# Запускаем CAI
cai  # первый запуск может занять до 30 секунд
```

### Ubuntu 20.04
```bash
sudo apt-get update && \
    sudo apt-get install -y software-properties-common

# Получаем Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev -y

# Создаём виртуальное окружение
python3.12 -m venv cai_env

# Устанавливаем пакет из локальной папки
source cai_env/bin/activate && pip install cai-framework

# Генерируем файл .env и заполняем значениями по умолчанию
echo -e 'OPENAI_API_KEY="sk-1234"\nANTHROPIC_API_KEY=""\nOLLAMA=""\nPROMPT_TOOLKIT_NO_CPR=1' > .env

# Запускаем CAI
cai  # первый запуск может занять до 30 секунд
```

### Windows WSL
Перейдите на страницу Microsoft: https://learn.microsoft.com/en-us/windows/wsl/install. Там вы найдёте все инструкции по установке WSL.

В Powershell выполните: wsl --install

```bash
sudo apt-get update && \
    sudo apt-get install -y git python3-pip python3-venv

# Создаём виртуальное окружение
python3 -m venv cai_env

# Устанавливаем пакет из локальной папки
source cai_env/bin/activate && pip install cai-framework

# Генерируем файл .env и заполняем значениями по умолчанию
echo -e 'OPENAI_API_KEY="sk-1234"\nANTHROPIC_API_KEY=""\nOLLAMA=""\nPROMPT_TOOLKIT_NO_CPR=1' > .env

# Запускаем CAI
cai  # первый запуск может занять до 30 секунд
```

### Android

Рекомендуем не менее 8 ГБ оперативной памяти:

1. Сначала установите UserLand: `https://play.google.com/store/apps/details?id=tech.ula&hl=es`

2. Установите минимальную версию Kali в базовых параметрах (бесплатно). [Или другую версию Kali, если предпочитаете]

3. Обновите ключи apt, как в этом примере: `https://superuser.com/questions/1644520/apt-get-update-issue-in-kali`. В терминале UserLand Kali выполните:

```bash
# Получаем новые ключи apt
wget http://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2024.1_all.deb

# Устанавливаем новые ключи apt
sudo dpkg -i kali-archive-keyring_2024.1_all.deb && rm kali-archive-keyring_2024.1_all.deb

# Обновляем репозиторий APT
sudo apt-get update

# CAI требует Python 3.12, установим его (CAI для Kali на Android)
sudo apt-get update && sudo apt-get install -y git python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev pkg-config
wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tar.xz
tar xf Python-3.12.4.tar.xz
cd ./configure --enable-optimizations
sudo make altinstall # Выполнение команды может занять много времени

# Клонируем исходники CAI
git clone https://github.com/aliasrobotics/cai && cd cai

# Создаём виртуальное окружение
python3.12 -m venv cai_env

# Устанавливаем пакет из локальной папки
source cai_env/bin/activate && pip3 install -e .

# Создаём файл .env и настраиваем его
cp .env.example .env  # измените здесь свои ключи/модели

# Запускаем CAI
cai
```

### Настройка файла `.env`

CAI использует файл `.env` для загрузки конфигурации при запуске. Чтобы упростить настройку, в репозитории есть примерный файл `.env.example`, который служит шаблоном для конфигурации CAI и ваших ключей API LLM.

```bash
OPENAI_API_KEY="sk-1234" 
# OPENAI_API_KEY ДОЛЖЕН БЫТЬ ЗАПОЛНЕН.
# Он должен содержать либо "sk-123" (как заполнителю), 
# либо ваш реальный API ключ. 
# Смотрите https://github.com/aliasrobotics/cai/issues/27

ANTHROPIC_API_KEY=""
OLLAMA=""
PROMPT_TOOLKIT_NO_CPR=1
```
⚠️ CAI НЕ предоставляет ключи API для каких-либо моделей по умолчанию.


### Поддержка пользовательского OpenAI Base URL
``` 
CAI поддерживает настройку собственного базового URL OpenAI API через переменную окружения `OPENAI_BASE_URL`. Это позволяет перенаправлять вызовы API на собственную конечную точку, например прокси или самохостимый сервис, совместимый с OpenAI.

Пример настройки в `.env`:
```
OLLAMA_API_BASE="https://custom-openai-proxy.com/v1"
```

Или напрямую из командной строки:
```bash
OLLAMA_API_BASE="https://custom-openai-proxy.com/v1" cai
```

