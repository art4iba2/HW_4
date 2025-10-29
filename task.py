from pydantic import BaseModel, field_validator
from typing import List


class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool
    categories: List[str] = []

    @field_validator("categories")
    def check_category_not_empty(cls, v):
        if any(not c.strip() for c in v):
            raise ValueError("Category cannot be empty")
        return v


class User(BaseModel):
    name: str
    email: str
    membership_id: str


def add_book(library_books: List["Book"], book: "Book") -> None:
        library_books.append(book)


def find_book(library_books: List["Book"], title: str) -> "Book | None":
    for book in library_books:
        if book.title.lower() == title.lower():
            return book
    return None


class BookNotAvailable(Exception):
    pass


def is_book_borrow(book: "Book") -> bool:
    if not book.available:
        raise BookNotAvailable(f"Книга '{book.title}' сейчас недоступна для выдачи.")
    book.available = False  # отмечаем как выданную
    return True


def return_book(book: "Book") -> None:
    book.available = True


class Library(BaseModel):
    books: List[Book]
    users: List[User]

    def total_books(self) -> int:
        return len(self.books)


library = Library(books=[], users=[])

book1 = Book(title="1984", author="Дж. Оруэлл", year=1949, available=True, categories=["антиутопия", "классика"])
book2 = Book(title="Война и мир", author="Л. Толстой", year=1869, available=False, categories=["роман", "история"])

add_book(library.books, book1)
add_book(library.books, book2)

user1 = User(name="Глеб Горбунов", email="gleb@example.com", membership_id="U001")
library.users.append(user1)

found = find_book(library.books, "1984")
print("Найдена книга:", found.title if found else "не найдена")

try:
    if is_book_borrow(found):
        print(f"Книга '{found.title}' взята.")
except BookNotAvailable as e:
    print("Ошибка:", e)

return_book(found)
print(f"Книга '{found.title}' возвращена.")

print("Всего книг в библиотеке:", library.total_books())
