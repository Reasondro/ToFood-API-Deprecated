# Dokumentasi API ToFood

Dokumen ini menyediakan instruksi tentang cara menggunakan endpoint API /api/token dan /api/protected-route. Endpoint ini digunakan untuk autentikasi dan mengakses sumber daya yang dilindungi.

## Daftar Isi

- Overview
- Endpoint Lists
- Contoh Pengugnaan dengna cURL
- Contoh Penggunaan dengan Postman

- Notes

## Overview

API ini menggunakan JSON Web Tokens (JWT) untuk autentikasi. Klien harus terlebih dahulu mendapatkan access token dengan menyediakan kredensial yang valid. Token ini kemudian digunakan untuk mengakses sumber daya yang dilindungi.

## Endpoint Lists

### 1. Mendapatkan Token Akses `(/api/token)`

- Deskripsi: Endpoint ini digunakan untuk otentikasi pengguna. Pengguna mengirimkan username dan password, dan jika kredensial valid, server akan mengembalikan token akses (JWT) yang dapat digunakan untuk mengakses endpoint yang dilindungi.

- PATH: `/api/token`
- Metode HTTP: `POST`
- Header:
  - `Content-Type: application/x-www-form-urlencoded`
- Body Parameters : Menggunakan form data (sebagai application/x-www-form-urlencoded):

  - `username` : string
  - `password` : string

- Contoh Request :

```http
POST /api/token HTTP/1.1
Host: https://tofood.azurewebsites.net
Content-Type: application/x-www-form-urlencoded

username=diddy&password=secret

```

- Respons Berhasil :

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

Di mana <JWT_TOKEN> adalah token JWT yang harus digunakan untuk mengakses endpoint yang dilindungi.

- Respons Gagal (401) :

```json
{
  "detail": "Invalid credentials"
}
```

Ini berarti username atau password yang diberikan tidak valid.

### 2. Mengakses Endpoint yang Dilindungi `(/api/protected-route)`

- Deskripsi: Endpoint ini hanya dapat diakses oleh pengguna yang telah otentikasi dan memiliki token akses yang valid. Token harus dikirimkan dalam header `Authorization` sebagai bearer token.

- PATH: `/api/protected-route`
- Metode HTTP: `GET`
- Header:

  - `Authorization: Bearer <JWT_TOKEN>`
    Ganti `<JWT_TOKEN>` dengan token akses yang didapat dari endpoint `/api/token`.

- Body Parameters : Tidak ada parameter tambahan

- Contoh Request :

```http
GET /api/protected-route HTTP/1.1
Host: https://tofood.azurewebsites.net
Authorization: Bearer <JWT_TOKEN>

```

- Respons Berhasil :

```json
{
  "message": "Hello, diddy!"
}
```

Di mana `diddy` adalah username dari pengguna yang telah otentikasi.

- Respons Gagal (401) :

```json
{
  "detail": "Could not validate credentials"
}
```

Ini berarti token yang diberikan tidak valid, telah kadaluarsa, atau tidak diberikan sama sekali.

## Contoh Penggunaaan dengan cURL

### 1. Mendapatkan Access Token

```bash
curl -X POST "https://tofood.azurewebsites.net/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=diddy&password=secret"
```

Respon:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

### 2. Mengakses Endpoint yang Dilindungi

```bash
curl -X GET "https://tofood.azurewebsites.net/api/protected-route" \
     -H "Authorization: Bearer <JWT_TOKEN>"
```

Respon:

```json
{
  "message": "Hello, diddy!"
}
```

## Contoh Penggunaan dengan Postman

### 1. Mendapatkan Access Token

- Metode: `POST`
- URL: `https://tofood.azurewebsites.net/api/token`
- Headers: `Content-Type` : `application/x-www-form-urlencoded`
- Body (x-www-form-urlencoded):
  - `username` : `diddy`
  - `password` : `secret`

Respon:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

### 2. Mengakses Endpoint yang Dilindungi

- Metode: `GET`
- URL: `https://tofood.azurewebsites.net/api/protected-route`
- Headers: `Authorization` : `Bearer <JWT_TOKEN>`

Respon:

```json
{
  "message": "Hello, diddy!"
}
```

## Catatan

- Pengguna yang Tersedia:

Saat ini, API menggunakan database dummy dengan satu pengguna:
_ Username: `diddy`
_ Password: `secret`

Jika ingin menambahkan pengguna baru, Anda dapat mengedit dictionary dummy_users_db di kode:

```python
dummy_users_db = {
    "diddy": {
        "username": "diddy",
        "hashed_password": pwd_context.hash("secret"),
    },
    "user_baru": {
        "username": "user_baru",
        "hashed_password": pwd_context.hash("password_baru"),
    }
}
```
