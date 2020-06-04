create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "products", true, "продукты, еда"),
    ("coffee", "coffee", true, "кофе, латте"),
    ("dinner", "dinner", true, "обед, столовая, ланч, бизнес-ланч, бизнес ланч"),
    ("cafe", "cafe", true, "кафе, ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio, burger king"),
    ("transport", "transport", false, "транспорт, метро, автобус, metro"),
    ("taxi", "taxi", false, "такси, яндекс такси, yandex taxi, uber,"),
    ("phone", "phone", false, "телефон, теле2, связь"),
    ("books", "books", false, "книги, литература, литра, лит-ра"),
    ("internet", "internet", false, "интернет, инет, inet"),
    ("subscriptions", "subscriptions", false, "подписки, подписка"),
    ("other", "other", true, "прочее, другое");

insert into budget(codename, daily_limit) values ('base', 500);