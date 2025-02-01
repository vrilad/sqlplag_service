# Спецификация API

Этот API предназначен для проверки кода SQL-запросов на плагиат. Он принимает SQL-запрос и возвращает процент его схожести с другим запросом.  

## Endpoints  

### Проверка на плагиат  

**Endpoint:**  `/check/`  

**Methods:**  `GET`, `POST`

**Body:**
```json
{
	"ref_code":"Select ship, count(ship) From Outcomes Group by ship Having count(ship) > 1",
  	"candidate_code": "SELECT ship, count(ship) as count_ship from Outcomes Group by ship Having count(ship) >1"
}
```

### Responses

-  **200 OK**: Возвращает процент сходства между запросами.

```json

{

"percent": "95.0"

}
```
-  **400 Bad Request**: Ошибка валидации запроса.