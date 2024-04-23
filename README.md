### Route Requests and Responses

1. User Registration Route : 
```javascript
        {
            request : POST,
            url : /api/auth/register/,
            required : [email, password]
        }
```
2. User Login Route : 
```javascript
        {
            request : POST,
            url : /api/auth/login/,
            required : [email, password]
        }
```
3. add user details : 
```javascript
        {
            request : POST,
            url : /api/user-details/data/,
            /* if user is vegitarian pass veg to the db and user isn't vegitarian pass non-veg to the db */
            required : [email, name, profile, birthday, gender, height, weight, diabetics_score, veg_status]
        }
```
4. get user details :
```javascript
        {
            request : POST,
            url : /api/user-details/data/get/,
            required : [email]
        }
```
5. update user details :
```javascript
        {
            request : PUT,
            url : /api/user-details/data/,
            /* if user is vegitarian pass veg to the db and user isn't vegitarian pass non-veg to the db */
            required : [email, name, profile, birthday, gender, height, weight, diabetics_score, veg_status]
        }
```
6. History Push :
```javascript
        {
            request : POST,
            url : /api/history/add/,
            required : [email, diabetics_score, weight, calories, carbs, fat, proteins]
        }
```
7. History Get :
```javascript
        {
            request : POST,
            url : /api/history/get/,
            required : [email]
        }
```
8. Get food recomendation:
```javascript
        {
            request : POST,
            url : /api/foods/get/,
            required : [email]
        }
```

9. Get resturent recomendation:
```javascript
        {
            request : POST,
            url : /api/resturents/get/,
            required : [city]
        }
```

10. Get meal recomendation:
```javascript
        {
            request : POST,
            url : /api/foods/get/meal/,
            required : [email]
        }
```
11. User Self Delete : 
```javascript
        {
            request : POST,
            url : /api/auth/delete/,
            required : [email, password]
        }
```
12. Add Resturent review text : 
```javascript
        {
            request : POST,
            url : /api/comment/set/,
            required : [email, hotel_id, comment]
        }
```
13. get Resturent reviews : 
```javascript
        {
            request : POST,
            url : /api/comment/get/,
            required : [hotel_id]
        }
```
13. get notifications : 
```javascript
        {
            request : POST,
            url : /api/notifications/get/,
            required : [email]
        }
```
14. set notifications : 
```javascript
        {
            request : POST,
            url : /api/notifications/set/,
            required : [email, notification, description]
        }
```
15. mark as read notifications : 
```javascript
        {
            request : PUT,
            url : /api/notifications/set/,
            required : [id]
        }
```