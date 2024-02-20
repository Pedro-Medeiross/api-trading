<h1>Api Investing Brazil</h1>

## Sobre este aplicativo
<p>Este projeto é uma Api de um projeto que fazia cadastro de usuários e cadastro e controle de transações que eram feitas em plataforma de "investimento" online, o mesmo aceitava cadastrar uma cotação que seria posteriormente validada por outro serviço, controlar se ela ja tinha sido agendada, executada ou cancelada por cada usuário. </p>

## Requisitos
### Python 3.11

## Instalação e configuração
Para instalar as dependências do projeto, execute o seguinte comando:

    pip install -r requirements.txt

Antes de executar a aplicação, é necessário criar as seguintes variáveis de ambiente:

<ul>
<li> DB_HOST: endereço do banco de dados </li>
<li> DB_NAME: nome do banco de dados </li>
<li> DB_PORT: porta do banco de dados </li>
<li> DB_USER: usuário do banco de dados </li>
<li> DB_PASSWORD: senha do usuário do banco de dados </li>
</ul>

Essas variáveis podem ser definidas no arquivo .env, seguindo o exemplo do arquivo .env.example.

## Utilização

### rodar o programa :

uvicorn main:app --reload

---

## About this app
<p>This project is an API from a system that used to register users and manage transactions made on an "investment" online platform. It allowed the registration of a quote that would be later validated by another service, keeping track of whether it had been scheduled, executed, or canceled by each user.</p>

## Requirements
### Python 3.11

## Installation and Configuration
To install the project dependencies, execute the following command:

    pip install -r requirements.txt


Before running the application, it is necessary to create the following environment variables:

<ul>
<li>DB_HOST: database address</li>
<li>DB_NAME: database name</li>
<li>DB_PORT: database port</li>
<li>DB_USER: database user</li>
<li>DB_PASSWORD: database user's password</li>
</ul>

These variables can be defined in the .env file, following the example from the .env.example file.

## Usage

### Run the program:

uvicorn main:app --reload
