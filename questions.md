a) For each pair of tables below, state the type of relationship
(one-to-one, one-to-many, or many-to-many) and briefly explain your reasoning.

i. Members → Loans: One-to-many relationship
Each member can borrow multiple times, but each borrowing record belongs to only one member
ii. Books → Loans: One-to-many relationship
Each book can be borrowed multiple times, but each borrowing record only corresponds to one book
iii. Members ↔ Books: Many-to-many relationship
Through indirect association via the Loans table, one member can borrow multiple books, and one book can also be borrowed by multiple members

b) A query joins members to loans using an INNER JOIN.

i. INNER JOIN effect
Members who have never borrowed books will be filtered out, and the result set will only include members with borrowing records
ii. After switching to LEFT JOIN
All members will be displayed, and members without borrowing records will have their loan fields displayed as NULL

c) The head librarian would like to see how many books have been borrowed by each library member.

SELECT 
    m.member_name,
    COUNT(l.loan_id) AS total_loans
FROM members m
LEFT JOIN loans l ON m.member_id = l.member_id
GROUP BY m.member_id, m.member_name
ORDER BY total_loans DESC;

d) The head librarian asks:
“Why don’t you store the book title with the loan? Wouldn’t that make it easier to see the data?”

The number of times a book is borrowed must be recorded as many times as the book title is saved, which wastes space. Moreover, if the title of the book is changed, all related records need to be updated. If a record is omitted, it will lead to different book titles appearing in different borrowing records in the system