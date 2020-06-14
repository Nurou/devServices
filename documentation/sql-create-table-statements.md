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

create table if not exists developer_skills
(
	developer_id integer
		constraint developer_skills_developer_id_fkey
			references developer,
	service_id integer
		constraint developer_skills_service_id_fkey
			references service
);

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

create table order_developers
(
	order_id integer
		constraint order_developers_order_id_fkey
			references "order",
	developer_id integer
		constraint order_developers_developer_id_fkey
			references developer
);


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


create table service
(
	id serial not null
		constraint service_pkey
			primary key,
	date_created timestamp,
	date_modified timestamp,
	name varchar(100) not null
);


