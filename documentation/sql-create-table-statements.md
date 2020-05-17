CREATE TABLE public.role
(
id integer NOT NULL DEFAULT nextval('role_id_seq'::regclass),
name character varying(40) COLLATE pg_catalog."default" NOT NULL,
account_id integer NOT NULL,
CONSTRAINT role_pkey PRIMARY KEY (id),
CONSTRAINT role_name_key UNIQUE (name),
CONSTRAINT role_account_id_fkey FOREIGN KEY (account_id)
REFERENCES public.account (id) MATCH SIMPLE
ON UPDATE NO ACTION
ON DELETE NO ACTION
)

CREATE TABLE public.account
(
id integer NOT NULL DEFAULT nextval('account_id_seq'::regclass),
username character varying(20) COLLATE pg_catalog."default" NOT NULL,
email character varying(120) COLLATE pg_catalog."default" NOT NULL,
password character varying(60) COLLATE pg_catalog."default" NOT NULL,
date_created timestamp without time zone,
date_modified timestamp without time zone,
CONSTRAINT account_pkey PRIMARY KEY (id),
CONSTRAINT account_email_key UNIQUE (email),
CONSTRAINT account_username_key UNIQUE (username)
)
