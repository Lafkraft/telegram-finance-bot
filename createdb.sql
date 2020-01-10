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
    created date,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category(codename, name, is_base_expense, aliases) values
('products', 'продукты', 1, 'еда'),   
('coffee', 'кофе', 1, ''),   
('dinner', 'обед', 1, 'столовая, ланч, бизнес-ланч, бизнес ланч'),    
('cafe', 'кафе', 1, 'ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio'),    
('transport', 'общ. транспорт', 0, 'метро, автобус, metro'),
('taxi', 'такси', 0, 'яндекс такси, yandex taxi'),
('phone', 'телефон', 0, 'теле2, связь'),
('books', 'книги', 0, 'литература, литра, лит-ра'),
('internet', 'интернет', 0, 'инет, inet'),
('subscriptions', 'подписки', 0, 'подписка'),
('other', 'прочее', 1, '');

insert into budget(codename, daily_limit) values ('base', 500);


