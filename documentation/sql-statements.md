
# SQL Statements

Below is a list of some of the SQL statements for the creation of the database tables and the features listed in the [user stories](https://github.com/Nurou/devServices/blob/master/documentation/user-stories.md). Other sql queries are found in the codebase with the `@staticmethod` annotation - links to them:

- [find_clients_with_no_orders](https://github.com/Nurou/devServices/blob/3fe4195d88a25041c71be7141d348e4f1d5163ab/application/auth/models.py#L42-L64)
- [find_clients_and_orders](https://github.com/Nurou/devServices/blob/3fe4195d88a25041c71be7141d348e4f1d5163ab/application/auth/models.py#L66-L80)
- [find_developers_with_matching_skills](https://github.com/Nurou/devServices/blob/3fe4195d88a25041c71be7141d348e4f1d5163ab/application/developers/models.py#L33-L48)

---

# Create Table Statements

```sql
create table account
(
	id serial not null
		constraint account_pkey
			primary key,
	date_created timestamp,
	date_modified timestamp,
	name varchar(120) not null
		constraint account_name_key
			unique,
	email varchar(120) not null
		constraint account_email_key
			unique,
	username varchar(20) not null
		constraint account_username_key
			unique,
	password varchar(60) not null,
	role_id integer default 2 not null
		constraint account_role__fk
			references role
);
```

```sql
create table developer
(
	id serial not null
		constraint developer_pkey
			primary key,
	date_created timestamp,
	date_modified timestamp,
	name varchar(100) not null,
	experience_level integer,
	hourly_cost integer
);
```

```sql
create table if not exists developer_skills
(
	developer_id integer
		constraint developer_skills_developer_id_fkey
			references developer,
	service_id integer
		constraint developer_skills_service_id_fkey
			references service
);
```

```sql
create table "order"
(
	id serial not null
		constraint order_pkey
			primary key,
	date_created timestamp,
	date_modified timestamp,
	title varchar(100) not null,
	requirements text,
	account_id integer not null
		constraint order_account_id_fkey
			references account,
	complete boolean default false,
	service_id integer
		constraint "order_service_service.id_fk"
			references service
);
```

```sql
create table order_developers
(
	order_id integer
		constraint order_developers_order_id_fkey
			references "order",
	developer_id integer
		constraint order_developers_developer_id_fkey
			references developer
);
```


```sql
create table role
(
	id serial not null
		constraint role_pkey
			primary key,
	date_created timestamp,
	date_modified timestamp,
	name varchar(40) not null
		constraint role_name_key
			unique,
	account_id integer
		constraint role_account_id_fkey
			references account
);
```


```sql
create table service
(
	id serial not null
		constraint service_pkey
			primary key,
	date_created timestamp,
	date_modified timestamp,
	name varchar(100) not null
);
```

---

# Feature Queries

## Login

```sql
SELECT account.id AS account_id,
       account.date_created AS account_date_created,
       account.date_modified AS account_date_modified,
       account.name AS account_name,
       account.email AS account_email,
       account.username AS account_username,
       account.password AS account_password,
       account.role_id AS account_role_id
FROM account
WHERE account.username = %(username_1)s
LIMIT %(param_1)s
SELECT role.id AS role_id,
       role.date_created AS role_date_created,
       role.date_modified AS role_date_modified,
       role.name AS role_name
FROM ROLE
WHERE role.id = %(param_1)s

```

## Admin Specific

### Fetching Clients

```sql
SELECT Account.name,
       Account.email
FROM Account
LEFT JOIN "order" ON "order".account_id = Account.id
WHERE ("order".complete IS NULL
       OR "order".complete = FALSE)
GROUP BY Account.id
HAVING COUNT("order".id) = 0

```

### Fetching Orders

 **All**

```sql
SELECT "order".id AS order_id,
       "order".date_created AS order_date_created,
       "order".date_modified AS order_date_modified,
       "order".title AS order_title,
       "order".requirements AS order_requirements,
       "order".complete AS order_complete,
       "order".account_id AS order_account_id,
       "order".service_id AS order_service_id
FROM "order
```

**Individual**

```sql
SELECT "order".id AS order_id,
       "order".date_created AS order_date_created,
       "order".date_modified AS order_date_modified,
       "order".title AS order_title,
       "order".requirements AS order_requirements,
       "order".complete AS order_complete,
       "order".account_id AS order_account_id,
       "order".service_id AS order_service_id
FROM "order"
WHERE "order".id = %(param_1)s
```

### Marking Order As Complete

```sql
UPDATE "order"
SET date_modified=CURRENT_TIMESTAMP,
                  complete=%(complete)s
WHERE "order".id = %(order_id)s
```

### Fetching Developers

```sql
SELECT developer.id AS developer_id,
       developer.date_created AS developer_date_created,
       developer.date_modified AS developer_date_modified,
       developer.name AS developer_name,
       developer.experience_level AS developer_experience_level,
       developer.hourly_cost AS developer_hourly_cost
FROM developer
```

### Adding Developers

```sql
INSERT INTO developer (date_created, date_modified, name, experience_level, hourly_cost)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(name)s, %(experience_level)s, %(hourly_cost)s) RETURNING developer.id
```

### Fetching Services

```sql
SELECT service.id AS service_id,
       service.date_created AS service_date_created,
       service.date_modified AS service_date_modified,
       service.name AS service_name
FROM service
```

### Adding Services

```sql
INSERT INTO service (date_created, date_modified, name)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(name)s) RETURNING service.id
```

### Deleting Services

```sql
DELETE FROM service WHERE service.id = %(id)s
```

## Client Specific

### Account Update

```sql
UPDATE account
SET date_modified=CURRENT_TIMESTAMP,
                  email=%(email)s,
                  username=%(username)s
WHERE account.id = %(account_id)s

```
### Account Deletion

```sql
DELETE
FROM account
WHERE account.id = %(id)s
```

## View Orders

```sql
SELECT "order".id AS order_id,
       "order".date_created AS order_date_created,
       "order".date_modified AS order_date_modified,
       "order".title AS order_title,
       "order".requirements AS order_requirements,
       "order".complete AS order_complete,
       "order".account_id AS order_account_id,
       "order".service_id AS order_service_id
FROM "order"
WHERE %(param_1)s = "order".account_id
ORDER BY "order".date_created DESC
LIMIT %(param_2)s
OFFSET %(param_3)s
```

## New Order
```sql
INSERT INTO "order" (date_created,
                     date_modified,
                     title,
                     requirements,
                     complete,
                     account_id,
                     service_id)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(title)s, %(requirements)s, %(complete)s, %(account_id)s, %(service_id)s) RETURNING "order".id
```

## Update Order
```sql
UPDATE "order"
SET date_modified=CURRENT_TIMESTAMP,
                  title=%(title)s
WHERE "order".id = %(order_id)s
```

## Delete Order
```sql
DELETE FROM "order"
WHERE "order".id = %(id)s
```


