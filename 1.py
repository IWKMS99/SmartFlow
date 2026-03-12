import os
import argparse
from pathlib import Path

class CodebaseCollector:
    """Минимальный сборщик кодовой базы"""

    def __init__(self, output_file: str):
        self.output_file_path = Path(output_file).resolve()
        self.script_file_path = Path(__file__).resolve() if __file__ != '<stdin>' else None

        # Исключения директорий
        self.exclude_dirs = {
                                ".git", ".vs", ".idea", ".vscode",
                                "bin", "obj", "packages", "node_modules",
                                "publish", "dist", ".mvn", ".gitlab", "target",
                                ".gradle", "build", "gradle"
                            }


        # Расширения файлов для включения
        self.include_extensions = {
                                      ".cs", ".cshtml", ".razor", ".resx",
                                      ".json", ".xml", ".yml", ".yaml",
                                      ".md", ".txt", ".config", ".env", ".http",
                                      ".csproj", ".vbproj", ".fsproj", ".sln", ".gitignore", ".java", ".sh",
                                      ".css", ".js", ".ts", ".tsx", ".properties", ".sql", ".html", ".conf", ".js"
                                  }

        # Имена файлов без расширений для включения
        self.include_filenames_without_extension = {
                                                      "Dockerfile", "docker-compose", "Caddyfile", "Makefile",
                                                      "Jenkinsfile", "Vagrantfile", "Procfile", "Brewfile",
                                                      "Gemfile", "Rakefile", "Capfile", "Guardfile", "Berksfile"
                                                  }


        # Исключения конкретных файлов
        self.exclude_files = {
                                 "codebase_collector.log",
                                 "codebase.txt",
                                 "appsettings.Development.json",
                                 "launchSettings.json",
                                 "package-lock.json"
                             }

    def is_excluded_dir(self, dir_name: str) -> bool:
        """Проверяет, исключена ли директория"""
        return dir_name in self.exclude_dirs

    def is_relevant_file(self, file_path: Path) -> bool:
        """Проверяет релевантность файла"""
        if not file_path.is_file():
            return False

        # Исключаем сам скрипт и выходной файл
        if self.script_file_path and file_path.resolve() == self.script_file_path:
            return False
        if file_path.resolve() == self.output_file_path:
            return False

        # Исключаем служебные файлы
        if file_path.name in self.exclude_files:
            return False

        # Проверяем размер (макс 10MB)
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:
                return False
        except OSError:
            return False

        # Включаем по расширению
        if file_path.suffix.lower() in self.include_extensions:
            return True

        # Для файлов без расширения проверяем по имени файла
        if not file_path.suffix and file_path.name in self.include_filenames_without_extension:
            return True

        return False

    def generate_tree_structure(self, root_dir: str) -> str:
        """Генерирует дерево проекта"""
        root_path = Path(root_dir)
        tree_lines = [f"Структура проекта: {root_path.name}", ""]

        def add_tree_level(path: Path, prefix: str = "", is_last: bool = True):
            if path.is_dir() and self.is_excluded_dir(path.name):
                return

            connector = "└── " if is_last else "├── "
            if path.is_dir():
                tree_lines.append(f"{prefix}{connector}{path.name}/")
                next_prefix = prefix + ("    " if is_last else "│   ")

                try:
                    children = list(path.iterdir())
                    dirs = [p for p in children if p.is_dir()]
                    files = [p for p in children if p.is_file()]

                    all_items = sorted(dirs, key=lambda x: x.name.lower()) + \
                               [f for f in sorted(files, key=lambda x: x.name.lower())
                                if self.is_relevant_file(f)]

                    for i, item in enumerate(all_items):
                        is_last_item = (i == len(all_items) - 1)
                        add_tree_level(item, next_prefix, is_last_item)

                except PermissionError:
                    tree_lines.append(f"{next_prefix}[Доступ запрещен]")
            else:
                if self.is_relevant_file(path):
                    tree_lines.append(f"{prefix}{connector}{path.name}")

        add_tree_level(root_path)
        return "\n".join(tree_lines)

    def collect_codebase(self, root_dir: str, output_file: str):
        """Собирает кодовую базу в текстовый файл"""
        root_path = Path(root_dir).resolve()

        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Дерево проекта
            tree_structure = self.generate_tree_structure(str(root_path))
            outfile.write(tree_structure)
            outfile.write("\n\n" + "=" * 80 + "\n\n")

            # Содержимое файлов
            for current_dir, subdirs, files in os.walk(root_path):
                current_path = Path(current_dir)

                # Фильтруем исключенные директории
                subdirs[:] = [d for d in subdirs if not self.is_excluded_dir(d)]

                for file_name in sorted(files):
                    file_path = current_path / file_name

                    if self.is_relevant_file(file_path):
                        relative_path = file_path.relative_to(root_path)

                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                content = infile.read()

                                outfile.write(f"--- {relative_path} ---\n")
                                outfile.write(content)
                                outfile.write("\n\n")

                        except Exception:
                            continue

def main():
    parser = argparse.ArgumentParser(description="Минимальный сборщик кодовой базы")
    parser.add_argument('--source', '-s', type=str, default='.', help="Путь к проекту")
    parser.add_argument('--output', '-o', type=str, default='codebase.txt', help="Выходной файл")

    args = parser.parse_args()

    collector = CodebaseCollector(args.output)
    collector.collect_codebase(args.source, args.output)
    print(f"Готово: {args.output}")

if __name__ == '__main__':
    main()
