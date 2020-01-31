# Transactions API Rest

Implement and design a simple REST API

## Description

We need to a simple API that allow us to register users' transactions and have an overview of how are they using their money.
To do so, we want you to implement a REST API that:

1. Can create users by receiving: name, email and age. 

Example:
```
{"name": "Jane Doe", "email": "jane@email.com", "age": 23}
```

2. List all users and also and see the details of a specific user.


3. Can save users' transactions. Each transaction has: reference (unique), account, date, amount, type and category.

Example:
```
{"reference": "000051", "account": "S00099", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries"}
```

Constraints:

- A transaction reference is unique.
- There are only two type of transactions: inflow and outflow.
- All outflow transactions amounts are negative decimal numbers.
- All inflow transactions amounts are positive decimal numbers.
- We expect to receive transactions in bulk as well.
- The transactions we receive could be already in our system, thus we need to avoid duplicating them in our database.

## Goals

- Given an user id, we want to be able to see a summary by account that shows the balance of the account, 
total inflow and total outflows. It should be possible to specify a date range, if no date range is given all 
transactions should be considered.


Input:
```
[
 {"reference": "000051", "account": "C00099", "date": "2020-01-03", "amount": "-51.13", "type": "outflow", "category": "groceries"},
 {"reference": "000052", "account": "C00099", "date": "2020-01-10", "amount": "2500.72", "type": "inflow", category": "salary"},
 {"reference": "000052", "account": "C00099", "date": "2020-01-10", "amount": "-150.72", "type": "outflow", category": "transfer"},
 {"reference": "000054", "account": "C00099", "date": "2020-01-13", "amount": "-560.00", "type": "outflow", "category": "rent"},
 {"reference": "000689", "account": "S00012", "date": "2020-01-10", "amount": "150.72", "type": "inflow", "category": "savings"},
]
```

Output:
```
[
 {"account": "C00099", "balance": "1738.87", "total_inflow": "2500.72", "total_outflow": "-761.85"},
 {"account": "S00012", "balance": "150.72", "total_inflow": "150.72", "total_outflow": "0.00"},
]

```

- Given an user id, we want to be able to see a summary by category that shows the sum of amounts per transaction category:


Input:
```
[
 {"reference": "000051", "account": "C00099", "date": "2020-01-03", "amount": "-51.13", "type": "outflow", "category": "groceries"},
 {"reference": "000052", "account": "C00099", "date": "2020-01-10", "amount": "2500.72", "type": "inflow", category": "salary"},
 {"reference": "000052", "account": "C00099", "date": "2020-01-10", "amount": "-150.72", "type": "outflow", category": "transfer"},
 {"reference": "000054", "account": "C00099", "date": "2020-01-13", "amount": "-560.00", "type": "outflow", "category": "rent"},
 {"reference": "000689", "account": "S00012", "date": "2020-01-10", "amount": "150.72", "type": "inflow", "category": "savings"},
]
```

Output:
```
{"inflow": {"salary": "2500.72", "savings": "150.72"}, "outflow": {"groceries": "-51.13", "rent": "-560.00", "transfer": "-150.72"}}
```
