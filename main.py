from fasthtml.common import *
from datetime import datetime

db = database("data/milktrack.db")

customers = db.t.customer
milks = db.t.milk

if customers not in db.t:
    customers.create(dict(id=int, name=str), pk="id")

if milks not in db.t:
    milks.create(dict(id=int, liter=int, date=str, customer_id=int), pk="id")

Customers = customers.dataclass()
Milk = milks.dataclass()


@patch
def __ft__(self: Customers):
    print(self.id)
    return Label(
        self.name,
        Input(id="liter", placeholder="Liter", type="number"),
        Hidden(id="id", value=self.id),
    )


app, rt = fast_app(live=True)


@rt("/")
def get():
    # customers.insert(name="Kane williams")
    add = A("Add data", href="/add")
    return Titled("MilkTrack", Div(id="nav"), add)


@rt("/add")
def get():
    frm = Form(
        *customers(),
        Button("Submit"),
        action="/add",
        method="POST",
    )
    return Container(frm)


@dataclass
class Milk_data:
    liter: list[int]
    id: list[int]

    def __call__(self):
        return [{"customer_id": _id, "liter": l} for _id, l in zip(self.id, self.liter)]


@rt("/add")
def post(milk: Milk_data):
    date = datetime.now().strftime("%d-%m-%Y")
    for i in milk():
        milks.insert(liter=i["liter"], date=date, customer_id=i["customer_id"])
    return RedirectResponse("/", status_code=303)


serve()
