# sqlalchemy api 

## For query 

## For update
- using `session.query`
- detect change automatically 
```python
user = session.query(User).filter(User.id == 1).first()
user.name = "New Name"
user.age = 30

session.commit()
```

- bulk updating

```python
session.query(User).filter(User.age < 18).update(
    {User.status: "underage"}, synchronize_session=False
)
session.commit()

```
- note: with synchronize_session
    - = False: dont synchronization
    - = "fetch": fetch again row id 
    - = "evaluate": assess condition automatically (something fail)

- updating by `session.merge()`

```python
detached_user = User(id=1, name="Updated", age=25)
session.merge(detached_user)
session.commit()
```

- `Instance` + `Session.add()`

```python
user = session.get(User, 1)
user.name = "Another Name"

session.add(user)    # optional
session.commit()

```
## For delete

