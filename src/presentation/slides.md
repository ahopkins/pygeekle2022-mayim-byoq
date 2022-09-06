layout: true
class: typo, typo-selection

---

count: false
class: nord-dark, center, middle

.rect.height-35[
	.width-30[
		.center[
			![](assets/images/logo.png)
		]
	]
]

# 💧 .oc-blue-3[Mayim]:  Bring Your Own Query

#### Intro to the non-ORM SQL client

Adam Hopkins
.left.font-sm[
```python
start = datetime(2022, 9, 6, 13, 40, 0, tzinfo=ZoneInfo(key="Asia/Jerusalem"))
end = start + timedelta(minutes=30)
```
]
---

class: border-layout, nord-dark

.east.height-100.width-65.p-xxs.ml-m[
	.card.noborder.noround.m-0.width-100.height-100[
.font-sm[
```python
class Adam:

	def __init__(self):
		self.work = PacketFabric("Director of Software Engineering")
		self.oss = Sanic("Core Maintainer")
		self.home = Israel("Negev")

	async def run(self, inputs: Union[Pretzels, Coffee]) -> None:
		while True:
			await self.work.do(inputs)
			await self.oss.do(inputs)
		
	def sleep(self):
		raise NotImplemented
```
]
.left[

- [PacketFabric](https://packetfabric.com/) - .font-sm[Network-as-a-Service platform; private access to the cloud; secure connectivity between data centers ]
- [Sanic Framework](https://sanicframework.org/) - .font-sm[ Python 3.7+ `asyncio` enabled framework and server. Build fast. Run fast. ]
- [GitHub - /ahopkins](https://github.com/ahopkins)
- [Twitter - @admhpkns](https://twitter/admhpkns)
		]
	]
]
.west.width-30[
	.pt-xxl.ml-xxl[
		.width-100[
			.center[
				.width-80[
					![](assets/images/profile.png)
				]
				.width-80[
					![](assets/images/packetfabric.png)
				]
				.width-80[
					![](assets/images/sanic.png)
				]
			]
		]
	]
]

???

PacketFabric’s Network-as-a-Service platform weaves together a perfect solution for networking. It provides private
access to the cloud, secure connectivity between data centers, an easy on ramp to the secure internet all coupled with
network automation. It's built for the way we do business today. Plus, we were just named one of the Top Ten Hottest
Networking Startups by CRN Magazine,

---

class: nord-dark

# 💧 .oc-blue-3[Mayim]: Is it an ORM?

.block-middle.width-40[
... Yes ⛔

... No ⛔

... Kind of? 🤷‍♂️
]

```python
>>> await executor.select_all_foo()
[<Foo one>, <Foo two>, <Foo three>]
```

---

class: nord-dark

# What is an ORM?

| | ORM | Mayim |
|-|:---:|:-----:|
| Connect to remote datasource | ✅ ||
| Create connection pool | ✅ ||
| Execute queries | ✅ ||
| Transaction support | ✅ ||
| Maps DB data to Python objects | ✅ ||
| Maps Python objects to DB queries | ✅ ||


---

class: nord-dark

# Why is .oc-blue-3[Mayim] NOT an ORM?

| | ORM | Mayim |
|-|:---:|:-----:|
| Connect to remote datasource | ✅ | ✅ |
| Create connection pool | ✅ | ✅ |
| Execute queries | ✅ | ✅ |
| Transaction support | ✅ | ✅ |
| Maps DB data to Python objects | ✅ | 🏆 |
| Maps Python objects to DB queries | ✅ | ⛔ |


---

class: nord-dark

# 💧 .oc-blue-3[Mayim]: Is it an ORM?


> Mayim is a BYOQ, NOT ORM query runner and hydrator

.rect.height-35[
		.center[
			![](assets/images/mapping.png)
		]
]

---

class: nord-dark

# What does it look like?

.font-sm[
```sql
CREATE TABLE department (
  department_id NUMBER NOT NULL PRIMARY KEY,
)
CREATE TABLE employee (
  employee_id NUMBER NOT NULL PRIMARY KEY,
  name VARCHAR NOT NULL,
  department NUMBER NOT NULL FOREIGN KEY REFERENCES department(id)
)
```
]
--
.font-sm[
```python
class Department:
	department_id: int
	employees: List[Employee]

    def get(self, department_id): ...

 
class Employee {
	employee_id: int
	name: str
	department: Department

    def get(self, employee_id): ...
```
]

---

class: nord-dark

```python
import asyncio
from mayim import Mayim, SQLiteExecutor, query
from dataclasses import dataclass


@dataclass
class Person:
    name: str


class PersonExecutor(SQLiteExecutor):
    @query("SELECT $name as name")
    async def select_person(self, name: str) -> Person:
        ...


async def run():
    executor = PersonExecutor()
    Mayim(db_path="./example.db")
    print(await executor.select_person(name="Adam"))


asyncio.run(run())
```

---

class: nord-dark, middle, center

# But ... writing SQL in strings is not fun 😫

.left[
```python{2}
class PersonExecutor(SQLiteExecutor):
*   @query("SELECT $name as name")
    async def select_person(self, name: str) -> Person:
        ...
```
]

---

class: nord-dark, middle, center

.rect.height-35[
		.center[
			![](assets/images/betterway.jpg)
		]
]

---

class: nord-dark

# Sample project structure

```python
./project
├── queries
│   └── select_all_cities.sql
└── basic.py
```

---

class: nord-dark

# First, the SQL

.rect.height-35[
		.center[
			![](assets/images/select_city_sql.png)
		]
]

---

class: nord-dark

# Second, create a model

```python
from dataclasses import dataclass


@dataclass
class City:
    id: int
    name: str
    countrycode: str
    district: str
    population: int
```

---

class: nord-dark

# Third, define an executor

```python
from mayim import PostgresExecutor


class CityExecutor(PostgresExecutor):
    async def select_all_cities(
        self, limit: int = 4, offset: int = 0
    ) -> List[City]:
        ...
```

---

class: nord-dark

# Third, define an executor, and run it

```python
from mayim import PostgresExecutor


class CityExecutor(PostgresExecutor):
    async def select_all_cities(
        self, limit: int = 4, offset: int = 0
    ) -> List[City]:
        ...
```
```python
async def run():
    executor = CityExecutor()
    Mayim(dsn="postgres://postgres:postgres@localhost:5432/world")
    print(await executor.select_all_cities())

asyncio.run(run())
```

---

class: nord-dark, middle


```python
[
    City(id=1, name='Kabul', countrycode='AFG', district='Kabol', population=1780000),
    City(id=2, name='Qandahar', countrycode='AFG', district='Qandahar', population=237500),
    City(id=3, name='Herat', countrycode='AFG', district='Herat', population=186800),
    City(id=4, name='Mazar-e-Sharif', countrycode='AFG', district='Balkh', population=127800)
]
```

---

class: nord-dark

# Why write my own SQL?

.font-sm[
- ORMs work well *if* strong object model, but breakdown with higher complexity
- ORMs lack easy insight into *what* is happening under the hood
- Every ORM has its own framework, and patterns to be learned
    - avoiding **N+1**
    - pagination
    - object proxies
    - aggregation strategies
- Do you want?
    - foreign data wrappers
    - stored procedures
    - highly nested and complex operations
    - use built-in functions
    - higher control of data access patterns
]

---

class: nord-dark

# Why write my own SQL?

```python
from pydantic import BaseModel

class City(BaseModel):
    id: int
    name: str
    district: str
    population: int


class Country(BaseModel):
    code: str
    name: str
    continent: str
    region: str
    capital: City
```

---

class: nord-dark

# Why write my own SQL?

.rect.height-35[
	.width-77[
		.center[
			![](assets/images/nested_object_sql.png)
		]
    ]
]

---

class: nord-dark

# Why write my own SQL?

.font-xs[
```python
[
    Country(
        code="AFG",
        name="Afghanistan",
        continent="Asia",
        region="Southern and Central Asia",
        capital=City(id=1, name="Kabul", district="Kabol", population=1780000),
    ),
    Country(
        code="ALB",
        name="Albania",
        continent="Europe",
        region="Southern Europe",
        capital=City(id=34, name="Tirana", district="Tirana", population=270000),
    ),
    Country(
        code="DZA",
        name="Algeria",
        continent="Africa",
        region="Northern Africa",
        capital=City(id=35, name="Alger", district="Alger", population=2168000),
    ),
    ...
]
```
]

---

class: nord-dark

# The possibilities are limitless ... 😎

.rect.height-35[
	.width-95[
		.center[
			![](assets/images/recursive_sql.png)
		]
    ]
]

---

class: nord-dark

# This thing called an `Executor`

```python
from mayim import PostgresExecutor
class CityExecutor(PostgresExecutor):
    async def select_all_cities(
        self, limit: int = 4, offset: int = 0
    ) -> List[City]:
        ...
```

--

**GOAL:** *To provide SQL execution with **first-class** treatment* 🥇

---

class: nord-dark, middle

```python
from mayim import PostgresExecutor

class SomeExecutor(PostgresExecutor):
    verb_prefixes = ...  # Default: select_,insert_,update_,delete_
    generic_prefix = ...  # Default: mayim_
    path = ...  # Default: ./queries
```

---

class: nord-dark, middle

```python
class CityExecutor(PostgresExecutor):


    async def select_city(self, ident: int | str, by_id: bool) -> City:
        query = "SELECT * FROM city"
        if by_id:
            query += "WHERE id = $ident"
        else:
            query += "WHERE name = $ident"
        return await self.execute(
            query,
            as_list=False,
            allow_none=False,
            params={"ident": ident}
        )
```

---

class: nord-dark, middle

```python
class CityExecutor(PostgresExecutor):
    generic_prefix: str = "fragment_"

    async def select_city(self, ident: int | str, by_id: bool) -> City:
        query = self.get_query("fragment_select_city")
        if by_id:
            query += self.get_query("fragment_where_id")
        else:
            query += self.get_query("fragment_where_name")
        return await self.execute(
            query,
            as_list=False,
            allow_none=False,
            params={"ident": ident}
        )
```

---

class: nord-dark

# What is a `Hydrator`? 🥤


> An object that turns a `dict` into a model

--

```python
from mayim import Hydrator

class CityHydrator(Hydrator):
    def hydrate(
        self, data: Dict[str, Any], model: Type[object] = City
    ) -> City:
        data["population"] = round(data["population"] / 1_000_000, 2)
        return model(**data)
```

---

class: nord-dark

# 💧 Mayim 💗 loves Pydantic


.font-xs[
```python
import asyncio
from mayim import Mayim, SQLiteExecutor, query
from pydantic import BaseModel


class Person(BaseModel):
    name: str


class PersonExecutor(SQLiteExecutor):
    @query("SELECT $name as name")
    async def select_person(self, name: str) -> Person:
        ...


async def run():
    executor = PersonExecutor()
    Mayim(db_path="./example.db")
    print(await executor.select_person(name="Adam"))


asyncio.run(run())
```

*(This script is complete, it should run "as is")*
]

---

class: nord-dark, middle

```python
class MarshmallowHydrator(Hydrator):
    def hydrate(self, data: Dict[str, Any], model: Type[Schema] = ...):
        schema = model()
        return schema.load(data)


async def run()
    Mayim(hydrator=MarshmallowHydrator(), ...)
```
---

class: nord-dark, middle

```python
from mayim import Mayim, Executor, Hydrator, hydrator

class HydratorA(Hydrator):
    ...

class HydratorB(Hydrator):
   ...

class SomeExecutor(Executor):
    async def select_a(...) -> Something:
        ...

    @hydrator(HydratorB())
    async def select_b(...) -> Something:
        ...

Mayim(executors=[SomeExecutor(hydrator=HydratorA())])
```

---

class: nord-dark, middle, center

# That's great, but... *How do I use it?*

---

class: nord-dark

# With .oc-pink-7[**Sanic**] Extensions

.font-sm[
```python
from mayim.extensions import SanicMayimExtension
from sanic_ext import Extend

class CityExecutor(Executor):
    async def select_all_cities(
        self, limit: int = 4, offset: int = 0
    ) -> List[City]:
        ...


app = Sanic(__name__)
Extend.register(
    SanicMayimExtension(
        executors=[CityExecutor], dsn="postgres://..."
    )
)


@app.get("/")
async def handler(request: Request, executor: CityExecutor):
    cities = await executor.select_all_cities()
    return json({"cities": [asdict(city) for city in cities]})
```
]
---

class: nord-dark

# Also for **Quart** and **Starlette**

.font-xs[
```python
from quart import Quart
from mayim.extension import QuartMayimExtension

app = Quart(__name__)

QuartMayimExtension(
    executors=[CityExecutor],
    dsn="postgres://postgres:postgres@localhost:5432/world",
).init_app(app)
```

```python
from starlette.applications import Starlette
from mayim.extension import StarletteMayimExtension

app = Starlette(routes=some_routes)

StarletteMayimExtension(
    executors=[CityExecutor],
    dsn="postgres://postgres:postgres@localhost:5432/world",
).init_app(app)
```
]

---

class: nord-dark, middle, center

GitHub - [/ahopkins]()<br />
Twitter - [@admhpkns]()<br />
PacketFabric - [packetfabric.com](https://packetfabric.com/)<br />
.oc-blue-3[Mayim] homepage - [ahopkins.github.io/mayim](https://ahopkins.github.io/mayim)<br />
.oc-blue-3[Mayim] repo - [/ahopkins/mayim](https://github.com/ahopkins/mayim)

.rect.height-35[
    .width-20[
		.center[
			![](https://sanicbook.com/images/SanicCoverFinal.png)
		]
	]
]

[**https://.oc-pink-7[sanicbook].com**](https://sanicbook.com/)
