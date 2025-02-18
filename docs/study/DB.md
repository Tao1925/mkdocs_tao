# 一、计划
## 阶段一：数据库基础

### **Day 1：数据库基础概念与安装**
**理论（1.5小时）**  
1、 数据库基本概念：数据库、表、字段、记录、数据类型（数值、字符串、日期等）。  

#### 数据库(database)  
**概念**: 数据库是一个结构化的数据集合，用于存储和管理数据。  

**基本操作**  
创建数据库 `CREATE DATABASES 数据库名;`  
使用数据库 `USE DATABASES 数据库名;`  
查看数据库 `SHOW DATABASES 数据库名;`  
删除数据库 `DROP DATABASES 数据库名;`（操作不可逆！）  
修改数据库  
```sql
ALTER DATABASE 数据库名 
CHARACTER SET = utf8mb4 --字符集
COLLATE = utf8mb4_unicode_ci; --排序方式
```
**QA**  
Q: 为什么不能直接在表中放数据，要加一层数据库？  
A: 相比直接在表中存数据，数据库提供了以下功能    

* 数据组织：将数据按逻辑结构存储，便于管理和访问。  
* 数据共享：多个应用程序可以同时访问同一个数据库。  
* 数据一致性：通过约束（如主键、外键）保证数据的完整性和一致性。  
* 数据安全：通过权限管理控制用户对数据的访问。  
* 高效查询：通过索引和优化技术提高数据检索效率。  

        


#### 表(table)
**概念**: 表是数据库中存储数据的基本单位，由 行（记录） 和 列（字段） 组成。  

* 行(Row/Record)：表中的一条记录，表示一个实体的信息。  
* 列(Column/Field)：表中的一个字段，表示实体的某个属性。  

**基本操作**  

创建表
```sql
CREATE TABLE 表名 (
    列名1 数据类型 [约束条件],
    列名2 数据类型 [约束条件],
    ...
    [表级约束条件]
);
示例:
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- 主键，自增
    name VARCHAR(50) NOT NULL,          -- 非空字符串
    age INT,                            -- 整数
    class VARCHAR(20)                   -- 字符串
);
```

查看表结构  `DESC 表名;`  

插入数据
```sql
INSERT INTO 表名 (列1, 列2, ...) 
VALUES (值1, 值2, ...);
示例:
INSERT INTO students (name, age, class) 
VALUES ('张三', 18, '高三(1)班');
```

查询数据
```sql
SELECT 列1, 列2, ... 
FROM 表名 
[WHERE 条件];
示例:
-- 查询所有学生的姓名和年龄
SELECT name, age FROM students;
-- 查询年龄大于 17 的学生
SELECT * FROM students WHERE age > 17;
```
更新数据
```sql
UPDATE 表名 
SET 列1 = 值1, 列2 = 值2, ... 
[WHERE 条件];
示例:
UPDATE students 
SET class = '高三(2)班' 
WHERE name = '张三';
```
删除数据
```sql
DELETE FROM 表名 
[WHERE 条件];
示例:
DELETE FROM students 
WHERE age < 16;
```



2、 数据库管理系统（DBMS）的作用和分类（关系型 vs 非关系型）。  


| 特性     | 关系型数据库（RDBMS）    | 非关系型数据库（NoSQL）         |
|----------|--------------------------|---------------------------------|
| 数据模型 | 表格形式（行和列）       | 键值对、文档、列族、图等形式    |
| 查询语言 | SQL                      | 特定的 API 或查询语言           |
| 事务支持 | 支持 ACID 事务           | 通常不支持 ACID，提供最终一致性 |
| 扩展性   | 垂直扩展（增加硬件性能） | 水平扩展（增加节点）            |
| 数据结构 | 固定，需要预先定义表结构 | 灵活，支持动态数据结构          |
| 一致性   | 强一致性                 | 最终一致性                      |
| 性能     | 适合复杂查询和事务操作   | 适合高并发和简单查询            |
| 适用场景 | 金融、ERP、传统业务系统  | 大数据、实时推荐、社交网络      |


3、 主键（Primary Key）、外键（Foreign Key）、索引（Index）的作用。  

#### 主键
**概念**: 是表中唯一标识一条记录的字段或字段组合。  

**作用**:  

* 唯一标识：确保每条记录的唯一性。
* 加速查询：主键默认会创建索引，提高查询效率。
* 数据完整性：防止插入重复数据或无效数据。

**特性**:  

* 唯一性：主键的值在表中必须是唯一的。
* 非空性：主键的值不能为 NULL。
* 不可修改：主键的值一旦确定，通常不建议修改。

**用法**:
```sql
CREATE TABLE 表名 (
    列名 数据类型 PRIMARY KEY,
    ...
);
示例:
-- 创建一个 `students` 表，`id` 列为主键
CREATE TABLE students (
    id INT PRIMARY KEY,  -- `id` 是主键
    name VARCHAR(50),
    age INT
);
```

**复合主键**:
```sql
CREATE TABLE 表名 (
    列1 数据类型,
    列2 数据类型,
    ...
    PRIMARY KEY (列1, 列2)  -- 复合主键
);
示例:
-- 创建一个 `enrollments` 表，`student_id` 和 `course_id` 组成复合主键
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)  -- 复合主键
);
```
#### 外键

**实践（1.5小时）**  

* 选择并安装一个数据库（推荐 **MySQL** 或 **PostgreSQL**）。
* 启动数据库服务，验证安装成功（通过命令行或图形化工具）。
* 尝试用命令行连接数据库（例如：`mysql -u root -p`）。

1、安装docker版本mysql
安装docker[在ubuntu上安装docker](https://docs.docker.com/engine/install/ubuntu/)  
拉取mysql的docker容器`sudo docker pull mysql:latest`
运行容器并设置端口映射与自启动
```sh
docker run --name mysql-study \
  -e MYSQL_ROOT_PASSWORD=secret_password \
  -p 3306:3306 \
  --restart=always \ 
  -d mysql:latest
```
2、使用图形化工具连接mysql
进入[navicat产品下载页面](https://www.navicat.com/en/products)，页面拉到最下，下载Navicat Premium Lite即可。


---

### **Day 2：SQL基础与DDL操作**
**理论（1小时）**
  - SQL语言分类：DDL（数据定义语言）、DML、DQL、DCL。
  - DDL语法：`CREATE DATABASE`、`CREATE TABLE`、`ALTER TABLE`、`DROP TABLE`。

**实践（2小时）**
  - 创建数据库：`CREATE DATABASE finance_db;`
  - 创建表（模拟金融场景）：
    ```sql
    CREATE TABLE customers (
        customer_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ```
  - 修改表结构：添加字段、删除字段、修改字段类型。

---

### **Day 3：DML操作与数据管理**
**理论（1小时）**
  - DML语法：`INSERT`、`UPDATE`、`DELETE`。
  - 事务的概念：`BEGIN`、`COMMIT`、`ROLLBACK`。

**实践（2小时）**
  - 向表中插入数据：
    ```sql
    INSERT INTO customers (name, email) 
    VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com');
    ```
  - 更新数据（例如：修改客户邮箱）。
  - 删除数据（例如：删除某条记录）。
  - 尝试事务操作：插入多条数据后回滚，观察结果。

---

### **Day 4：DQL查询基础**
**理论（1小时）**
  - `SELECT` 语句基础：`SELECT * FROM table`。
  - 条件过滤：`WHERE`、比较运算符（`=`, `>`, `<`）。
  - 排序：`ORDER BY`。

**实践（2小时）**
  - 查询表中所有数据。
  - 条件查询：查询特定客户（例如：`WHERE name = 'Alice'`）。
  - 排序：按创建时间降序排列客户列表。
  - 插入更多测试数据（至少20条），练习复杂查询。

---

### **Day 5：DQL高级查询**
**理论（1小时）**
  - 聚合函数：`COUNT`、`SUM`、`AVG`、`MAX`、`MIN`。
  - 分组统计：`GROUP BY`、`HAVING`。

**实践（2小时）**
  - 统计客户总数：`SELECT COUNT(*) FROM customers;`
  - 按邮箱域名分组统计客户数量：
    ```sql
    SELECT SUBSTRING_INDEX(email, '@', -1) AS domain, COUNT(*) 
    FROM customers 
    GROUP BY domain;
    ```
  - 筛选分组结果（例如：客户数超过5的域名）。

---

### **Day 6：表关系与JOIN操作**
**理论（1小时）**
  - 表关系：一对一、一对多、多对多。
  - 外键约束与关联查询：`INNER JOIN`、`LEFT JOIN`。

**实践（2小时）**
  - 创建关联表（例如：`accounts` 表关联 `customers`）：
    ```sql
    CREATE TABLE accounts (
        account_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT,
        balance DECIMAL(10, 2),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    ```
  - 插入账户数据，练习 `JOIN` 查询：
    ```sql
    SELECT c.name, a.balance 
    FROM customers c 
    INNER JOIN accounts a ON c.customer_id = a.customer_id;
    ```

---

### **Day 7：索引与查询优化**
**理论（1小时）**
  - 索引的作用和类型（B-Tree、Hash）。
  - 如何创建索引：`CREATE INDEX`。
  - 索引的优缺点（查询加速 vs 写操作性能损耗）。

**实践（2小时）**
  - 为 `customers` 表的 `email` 字段创建索引。
  - 对比有索引和无索引时的查询性能（使用 `EXPLAIN` 分析执行计划）。
  - 练习索引的删除和修改。

---

### **Day 8：数据库约束与数据完整性**
**理论（1小时）**
  - 约束类型：主键、外键、唯一约束（UNIQUE）、非空约束（NOT NULL）、检查约束（CHECK）。
  - 数据完整性的意义（避免脏数据）。

**实践（2小时）**
  - 创建带约束的表（例如：账户余额不允许为负数）：
    ```sql
    CREATE TABLE transactions (
        transaction_id INT PRIMARY KEY AUTO_INCREMENT,
        account_id INT,
        amount DECIMAL(10, 2) CHECK (amount > 0),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    );
    ```
  - 测试约束：尝试插入违反约束的数据，观察报错信息。

---

### **Day 9：图形化工具与数据导入导出**
**理论（0.5小时）**
  - 图形化工具的作用（Navicat、DBeaver、MySQL Workbench）。
  - 数据导入导出格式（CSV、SQL文件）。

**实践（2.5小时）**
  - 安装并配置一个图形化工具（推荐 **DBeaver**）。
  - 使用工具连接数据库，浏览表结构和数据。
  - 导出 `customers` 表数据为 CSV 文件，修改后重新导入。

---

### **Day 10：用户权限管理（DCL）**
**理论（1小时）**
  - 用户管理：`CREATE USER`、`DROP USER`。
  - 权限管理：`GRANT`、`REVOKE`。
  - 角色（Role）的概念。

**实践（2小时）**
  - 创建新用户并分配权限（例如：只允许查询 `customers` 表）。
  - 用新用户登录，测试权限限制。
  - 撤销权限并删除用户。

---

### **Day 11：综合练习1（设计小型金融数据库）**
**任务（3小时）**
  - 设计一个简单的金融数据库，包含以下表：
    - `customers`（客户信息）
    - `accounts`（账户信息，关联客户）
    - `transactions`（交易记录，关联账户）
  - 使用 SQL 脚本创建表，并插入测试数据。
  - 编写查询：统计每个客户的总交易金额。

---

### **Day 12：综合练习2（问题排查与优化）**
**任务（3小时）**
  - 人为制造数据库问题（例如：慢查询、死锁）。
  - 使用工具（如 `SHOW PROCESSLIST`、`EXPLAIN`）分析问题。
  - 优化查询语句或索引配置，解决问题。
  - 总结学习成果，记录未掌握的知识点。

---

### **工具与资源推荐**
1. **在线练习平台**：
   - SQLZoo（https://sqlzoo.net/）
   - LeetCode 数据库题库（https://leetcode.com/problemset/database/）
2. **本地环境**：
   - 使用 Docker 快速部署数据库（避免本地安装冲突）。
   - 示例命令：`docker run --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest`

---

### **关键学习要点**
- 每天完成实践后，记录遇到的问题和解决方案。
- 金融场景下的数据库设计需注重 **数据一致性** 和 **事务安全**。
- 后续阶段将深入性能优化和高可用方案，打好基础是关键！