# Title: Rubberduck groceries store (MVP)

---

## Overview

This will be a customer to customer (c2c) e-commerce of pets.

Mainly focused in the cart part and users creation. It also contains the
inventory managment.

### Scope

Basic user authentication and inventory management. Mainly focused in the cart feature.

#### Use cases

Customer to customer service, there will be two kind of users, regular
user, seller user. The seller user is a regular user with more permissions.

- [x] Sign up. A user registers to the site with email, username, password,
name, phonenumber, age, gender, and wether the user wants to sell or only
consume.
- [x] It is not necessary to be loged in to see all the available products.
- [x] It is necessary to be authenticated to add products to the cart.
- [x] The size of the pagination can be changed for 10, 20, or 30 products
per page.
- [x] Sign in. A user authenticates with its username and password and
receives a JWT token to sign all its requests that add or modify data.
- [x] A regular user does not have permission to add or modify products for
sell.
- [x] A seller user cannot modify products that are not owned (sold) by
that user.
- [x] All the products that have stock=0 and that are not sold by the current
user wont be returned by the API.
- [x] Only a seller can see products that he/she sells that have 0 existencies.
- [x] The user can search for a product with string. Uses search as query_param.
- [x] Only a seller can modify stock of owned products.
- [x] A seller user can also buy.
- [x] A regular user and a seller user can add, modify and delete products
of his/her cart.
- [x] The user cannot add more items to the cart than what is available.
- [x] The user cannot set the quantity of a product in the cart to 0 or less.
- [x] A seller user can see a register of all the completed purchases of his/her
products.

#### Out of Scope

This is an MVP therefore some features that would be nice to have in an
ecoommerce are not implemented. A few of them are

- [ ] Track of orders is not implemented
- [ ] Out of stock alerts are not implemented
- [ ] A real payment API like stripe is not consumed.
- [ ] Recomendations of products to the user.
- [ ] Order cancellation.

## Arquitecture (To be Updated)

### Diagrams

poner diagramas de secuencia, uml, etc

### Data models

[![Entity relation diagram](https://mermaid.ink/img/pako:eNqVVcFunDAQ_RWLc_IDXNuoSi6tVPWGhAY8AbfGdsdmo9XCv8deGwJetko5rPCb53lvPB72UrSaY1EWSF8FdARDpZh_fiANwlqhFbtEJDxCOSb4x9o6EqpjCgaM4Hyze54eH6cL-0Z6NKxkPdhIicD_5F5IZk2-0_xlkWwu16DUqrNbRpLcyiUpA9a-adqDo9-0qy9VSJqPrWNT1EvL5wE69LIcbUuiQV4352xHpByYuJYWOfWCGXA9E2FHJh9LSeIvevQW5ZNydPbi-k3ZQ5MZT6hKLfl2oawpPh9SvW0NB4dODMhaQv_Ks_5kRVx3YOvLkOzvCMoJdz4oZ3H5nbhflL72kCDGI3bn0Pb-grfaSGiRs-DROhhMDPl3b8L7rYFInDCPz3u5rZ9nh4P31GrlQCzH-xEJVD0dNyLn3qsiEOot8jtmqzGku71-r0Ji9Dhdzy_N1j5-Ryxc6p3WesPSre9Q0R4xvVaoxqFB-kfzlhtXMotS2nxaPtXBm8FPQBwq49bBb7SWDE4gJDQycZeLZki0GRQceZlN5LCEL0BuaTeouocTHk5TxmuwFus4rbHPnn8-MwHbz8o6c-GnBs6XsZuLh2Lwn0Q_Lv4zfhWsCtejP72i9K8c6E9VVCrwRhPSPHHhNBXlK0iLDwWMTv88q3YFIiv9HSR0fgcV4wVq)](https://mermaid.live/edit#pako:eNqVVcFunDAQ_RWLc_IDXNuoSi6tVPWGhAY8AbfGdsdmo9XCv8deGwJetko5rPCb53lvPB72UrSaY1EWSF8FdARDpZh_fiANwlqhFbtEJDxCOSb4x9o6EqpjCgaM4Hyze54eH6cL-0Z6NKxkPdhIicD_5F5IZk2-0_xlkWwu16DUqrNbRpLcyiUpA9a-adqDo9-0qy9VSJqPrWNT1EvL5wE69LIcbUuiQV4352xHpByYuJYWOfWCGXA9E2FHJh9LSeIvevQW5ZNydPbi-k3ZQ5MZT6hKLfl2oawpPh9SvW0NB4dODMhaQv_Ks_5kRVx3YOvLkOzvCMoJdz4oZ3H5nbhflL72kCDGI3bn0Pb-grfaSGiRs-DROhhMDPl3b8L7rYFInDCPz3u5rZ9nh4P31GrlQCzH-xEJVD0dNyLn3qsiEOot8jtmqzGku71-r0Ji9Dhdzy_N1j5-Ryxc6p3WesPSre9Q0R4xvVaoxqFB-kfzlhtXMotS2nxaPtXBm8FPQBwq49bBb7SWDE4gJDQycZeLZki0GRQceZlN5LCEL0BuaTeouocTHk5TxmuwFus4rbHPnn8-MwHbz8o6c-GnBs6XsZuLh2Lwn0Q_Lv4zfhWsCtejP72i9K8c6E9VVCrwRhPSPHHhNBXlK0iLDwWMTv88q3YFIiv9HSR0fgcV4wVq)

---

## Limitations

Some technologies constraints and utilities required for the design.

<!--
Ej.
* Llamadas del API tienen latencia X
* No se soporta mas de X llamadas por segundo
-->

### Technologies

- [x] Docker
- [x] Django
- [x] Django REST framework

### Utilities

- [x] Fixtures
  - Initial data is provided
- [x] Migrations
  - Added a barcode number. This field is unique needs special management
   in migrations.
- [x] Custom commands
  - Added the command intialexistences which creates a Journal Entry
   for adding len(product.name) existences to the the products that are
   initially available.
- [ ] Unit tests

## Instructions

Assuming internet connection a docker installed

1. Run  `docker-compose up --build -d` in the terminal
2. Enter to the container with `docker exec -it ecommerce-ecommerce-1 bash`
3. Move to the django app folder `cd rubberduck_store/`
4. Populate the db with initial data using `python manage.py migrate && python manage.py loaddata auth products`
5. Create registers for the initial product stock with `python manage.py intialexistences`

Now it is ready to test
