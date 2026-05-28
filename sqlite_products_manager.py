import sqlite3
from typing import List, Optional, Tuple


class ProductRepository:
    """
    장난감 상자처럼 제품 정보를 넣고 꺼내는 도우미 클래스예요.

    이 클래스는 컴퓨터 안에 있는 작은 저장 상자(SQLite 데이터베이스)를 사용해요.
    상자 이름은 기본으로 MyProduct.db이고, 그 안에 Products라는 표(테이블)를 만들어요.
    우리가 할 수 있는 일은 4가지예요.

    1) 넣기(INSERT): 새 제품을 추가해요.
    2) 고치기(UPDATE): 이미 있는 제품 정보를 바꿔요.
    3) 지우기(DELETE): 필요 없는 제품을 지워요.
    4) 찾기(SELECT): 저장된 제품을 읽어 와요.
    """

    def __init__(self, db_name: str = "MyProduct.db") -> None:
        """
        시작할 때 데이터베이스 준비를 해요.

        Args:
            db_name (str): 저장 상자(데이터베이스) 파일 이름이에요.
                아무것도 안 주면 "MyProduct.db"를 써요.

        쉬운 설명:
            집에서 장난감 상자 이름표를 붙이는 것처럼,
            여기서는 파일 이름을 정하고 표(테이블)도 만들어 둘 준비를 해요.
        """
        self.db_name = db_name
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        """
        데이터베이스 상자와 연결 줄을 만들어요.

        Returns:
            sqlite3.Connection: 데이터베이스와 대화할 수 있는 연결 객체예요.

        쉬운 설명:
            상자 안 물건을 꺼내려면 상자를 열어야 하죠?
            이 메서드는 상자를 여는 열쇠 같은 역할을 해요.
        """
        return sqlite3.connect(self.db_name)

    def _create_table(self) -> None:
        """
        Products라는 표(테이블)가 없으면 새로 만들어요.

        표 안에는 아래 3칸(컬럼)이 있어요.
        - productID: 제품 번호(숫자)
        - productName: 제품 이름(글자)
        - productPrice: 제품 가격(숫자)

        쉬운 설명:
            이름표가 붙은 서랍 3칸을 만든다고 생각하면 돼요.
            이미 있으면 다시 만들지 않고 그대로 써요.
        """
        query = """
        CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY,
            productName TEXT NOT NULL,
            productPrice INTEGER NOT NULL
        )
        """
        with self._connect() as conn:
            conn.execute(query)

    def insert_product(self, product_id: int, product_name: str, product_price: int) -> None:
        """
        제품 1개를 표에 새로 넣어요.

        Args:
            product_id (int): 제품 번호예요. (예: 1, 2, 3)
            product_name (str): 제품 이름이에요. (예: "청소기")
            product_price (int): 제품 가격이에요. (예: 50000)

        쉬운 설명:
            새 스티커를 한 장 만들어 상자 안 목록에 붙이는 일이에요.
        """
        query = """
        INSERT INTO Products (productID, productName, productPrice)
        VALUES (?, ?, ?)
        """
        with self._connect() as conn:
            conn.execute(query, (product_id, product_name, product_price))

    def insert_products_bulk(self, products: List[Tuple[int, str, int]]) -> None:
        """
        제품 여러 개를 한 번에 넣어요.

        Args:
            products (List[Tuple[int, str, int]]):
                (제품번호, 제품이름, 제품가격) 모양의 묶음 리스트예요.

        쉬운 설명:
            스티커를 한 장씩 붙이지 않고,
            스티커 묶음을 한 번에 쭉 붙이는 방법이에요.
        """
        query = """
        INSERT INTO Products (productID, productName, productPrice)
        VALUES (?, ?, ?)
        """
        with self._connect() as conn:
            conn.executemany(query, products)

    def update_product(self, product_id: int, product_name: str, product_price: int) -> int:
        """
        이미 있는 제품 정보를 새 값으로 고쳐요.

        Args:
            product_id (int): 어떤 제품을 고칠지 찾는 번호예요.
            product_name (str): 새 제품 이름이에요.
            product_price (int): 새 제품 가격이에요.

        Returns:
            int: 실제로 고쳐진 줄의 개수예요.
                1이면 잘 고친 것이고, 0이면 해당 번호를 못 찾은 거예요.

        쉬운 설명:
            붙어 있던 스티커 글자를 지우고 새 글자로 바꾸는 일이에요.
        """
        query = """
        UPDATE Products
        SET productName = ?, productPrice = ?
        WHERE productID = ?
        """
        with self._connect() as conn:
            cursor = conn.execute(query, (product_name, product_price, product_id))
            return cursor.rowcount

    def delete_product(self, product_id: int) -> int:
        """
        제품 1개를 표에서 지워요.

        Args:
            product_id (int): 지울 제품 번호예요.

        Returns:
            int: 실제로 지운 줄의 개수예요.
                1이면 잘 지운 것이고, 0이면 해당 번호가 없던 거예요.

        쉬운 설명:
            목록에서 필요 없는 스티커를 떼어내는 일이에요.
        """
        query = "DELETE FROM Products WHERE productID = ?"
        with self._connect() as conn:
            cursor = conn.execute(query, (product_id,))
            return cursor.rowcount

    def select_product(self, product_id: int) -> Optional[Tuple[int, str, int]]:
        """
        제품 번호로 제품 1개를 찾아서 보여줘요.

        Args:
            product_id (int): 찾고 싶은 제품 번호예요.

        Returns:
            Optional[Tuple[int, str, int]]:
                찾으면 (제품번호, 제품이름, 제품가격)을 돌려주고,
                못 찾으면 None을 돌려줘요.

        쉬운 설명:
            서랍에서 "1번 스티커 어디 있지?" 하고 찾아오는 일이에요.
        """
        query = "SELECT productID, productName, productPrice FROM Products WHERE productID = ?"
        with self._connect() as conn:
            cursor = conn.execute(query, (product_id,))
            return cursor.fetchone()

    def select_products(self, limit: int = 10) -> List[Tuple[int, str, int]]:
        """
        제품을 여러 개 읽어 와요.

        Args:
            limit (int): 몇 개까지 가져올지 정해요. 기본값은 10개예요.

        Returns:
            List[Tuple[int, str, int]]:
                [(제품번호, 제품이름, 제품가격), ...] 모양의 리스트예요.

        쉬운 설명:
            목록을 맨 위에서부터 몇 장만 살짝 넘겨서 보는 일이에요.
        """
        query = "SELECT productID, productName, productPrice FROM Products ORDER BY productID LIMIT ?"
        with self._connect() as conn:
            cursor = conn.execute(query, (limit,))
            return cursor.fetchall()

    def count_products(self) -> int:
        """
        지금 표 안에 제품이 몇 개인지 세어요.

        Returns:
            int: 저장된 제품 개수예요.

        쉬운 설명:
            상자 안에 스티커가 총 몇 장 있는지 세어 보는 일이에요.
        """
        query = "SELECT COUNT(*) FROM Products"
        with self._connect() as conn:
            cursor = conn.execute(query)
            return int(cursor.fetchone()[0])

    def seed_sample_data(self, count: int = 10000) -> None:
        """
        연습용 샘플 제품 데이터를 많이 만들어 넣어요.

        Args:
            count (int): 몇 개를 만들지 정해요. 기본값은 10000개예요.

        동작 방식:
            1) 먼저 Products 표를 깨끗이 비워요.
            2) 1번부터 count번까지 제품을 만들어요.
            3) 이름은 Product-번호, 가격은 규칙으로 만들어 넣어요.

        쉬운 설명:
            연습장에 문제를 풀기 전에,
            연습용 스티커 1만 장을 한 번에 준비하는 일이에요.
        """
        products = [
            (i, f"Product-{i}", 1000 + (i % 500) * 10)
            for i in range(1, count + 1)
        ]

        with self._connect() as conn:
            conn.execute("DELETE FROM Products")
            conn.executemany(
                "INSERT INTO Products (productID, productName, productPrice) VALUES (?, ?, ?)",
                products,
            )


if __name__ == "__main__":
    repo = ProductRepository("MyProduct.db")

    # Prepare 10,000 sample rows.
    repo.seed_sample_data(10000)
    print("Seeded rows:", repo.count_products())

    # INSERT example
    repo.insert_product(10001, "Product-10001", 19900)
    print("After insert:", repo.select_product(10001))

    # UPDATE example
    repo.update_product(10001, "Product-10001-Updated", 15000)
    print("After update:", repo.select_product(10001))

    # SELECT example
    print("Top 5 rows:", repo.select_products(5))

    # DELETE example
    repo.delete_product(10001)
    print("After delete:", repo.select_product(10001))
    print("Final row count:", repo.count_products())
