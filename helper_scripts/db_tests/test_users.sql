-- Generates the maker club database

-- Create the database test_db if it doesn't already exist
-- Use test_db
-- Create the table `users` if it doesn't already exist

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(60) PRIMARY KEY NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    username VARCHAR(60) NOT NULL DEFAULT '',
    profile_pic VARCHAR(256),
    email VARCHAR(128) UNIQUE NOT NULL,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128),
    country VARCHAR(60),
    postal_code VARCHAR(60)
);

INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('00', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '00@example.com', 'Alice', 'Adams', 'USA', '00000');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('01', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '01@example.com', 'Bobby', 'Barks', 'USA', '00001');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('02', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '02@example.com', 'Carly', 'Cuomo', 'USA', '00002');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('03', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '03@example.com', 'Devin', 'Dunst', 'USA', '00003');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('04', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '04@example.com', 'Erica', 'Evans', 'USA', '00004');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('05', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '05@example.com', 'Fancy', 'Fauci', 'USA', '00005');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('06', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '06@example.com', 'Gabby', 'Gomez', 'USA', '00006');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('07', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '07@example.com', 'Harry', 'Hanes', 'USA', '00007');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('08', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '08@example.com', 'Isaac', 'Ivans', 'USA', '00008');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('09', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '09@example.com', 'Josie', 'Jones', 'USA', '00009');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('10', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '10@example.com', 'Kevin', 'Klein', 'USA', '00010');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('11', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '11@example.com', 'Lizzy', 'Lizzo', 'USA', '00011');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('12', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '12@example.com', 'Manny', 'Marks', 'USA', '00012');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('13', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '13@example.com', 'Norma', 'Nuñez', 'USA', '00013');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('14', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '14@example.com', 'Oscar', 'Owens', 'USA', '00014');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('15', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '15@example.com', 'Paula', 'Paben', 'USA', '00015');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('16', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '16@example.com', 'Queen', 'Quare', 'USA', '00016');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('17', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '17@example.com', 'Rohan', 'Roche', 'USA', '00017');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('18', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '18@example.com', 'Sammy', 'Stein', 'USA', '00018');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('19', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '19@example.com', 'Terry', 'Tahoe', 'USA', '00019');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('20', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '20@example.com', 'Under', 'Water', 'USA', '00020');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('21', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '21@example.com', 'Vance', 'VvVvV', 'USA', '00021');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('22', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '22@example.com', 'Willy', 'Wonka', 'USA', '00022');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('23', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '23@example.com', 'X#éòç', '-$8nN', 'USA', '00023');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('24', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '24@example.com', 'Yanni', 'Yeezy', 'USA', '00024');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('25', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '25@example.com', 'Zenon', 'Zamor', 'USA', '00025');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('26', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '26@example.com', 'Artie', 'Alpha', 'USA', '00026');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('27', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '27@example.com', 'Betsy', 'Besty', 'USA', '00027');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('28', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '28@example.com', 'Candy', 'Crush', 'USA', '00028');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('29', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '29@example.com', 'Devil', 'Deeds', 'USA', '00029');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('30', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '30@example.com', 'Extra', 'Extra', 'USA', '00030');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('31', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '31@example.com', 'Faith', 'Facts', 'USA', '00031');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('32', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '32@example.com', 'Gordo', 'Gomez', 'USA', '00032');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('33', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '33@example.com', 'Hahah', 'ahaha', 'USA', '00033');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('34', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '34@example.com', 'Isaac', 'Isaac', 'USA', '00034');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('35', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '35@example.com', 'Jason', 'J SON', 'USA', '00035');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('36', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '36@example.com', 'Kerry', 'Karry', 'USA', '00036');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('37', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '37@example.com', 'Laura', 'Lopez', 'USA', '00037');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('38', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '38@example.com', 'Mephistopheles the 2nd', '', 'USA', '00038');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('39', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '39@example.com', 'Nexus', 'Nodes', 'USA', '00039');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('40', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '40@example.com', 'Oscar', 'O\'neal', 'USA', '00040');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('41', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '41@example.com', 'Peter', 'Parks', 'USA', '00041');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('42', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '42@example.com', 'Q', 'Anon', 'USA', '00042');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('43', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '43@example.com', 'Ricky', 'Rubio', 'USA', '00043');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('44', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '44@example.com', 'Stale', 'Stail', 'USA', '00044');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('45', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '45@example.com', 'Terry', 'Tacos', 'USA', '00045');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('46', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '46@example.com', 'Under', 'Over Jr.', 'USA', '00046');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('47', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '47@example.com', 'Vince', 'McVan', 'USA', '00047');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('48', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '48@example.com', 'Wanda', 'Wu', 'USA', '00048');
INSERT INTO `users` (`id`, `created_at`, `updated_at`, `email`, `first_name`, `last_name`, `country`, `postal_code`) VALUES ('49', '1000-01-01 00:00:00', '1000-01-01 00:00:00', '49@example.com', 'J.I.', 'Cruz', 'USA', '00049');
