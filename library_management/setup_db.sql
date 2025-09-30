-- Create and use database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS issue_history;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

-- Users table for authentication
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_date DATE DEFAULT (CURRENT_DATE)
);

-- Books table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    total INT NOT NULL DEFAULT 1,
    available INT NOT NULL DEFAULT 1,
    added_date DATE DEFAULT (CURRENT_DATE)
);

-- Students table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    enrollment_date DATE DEFAULT (CURRENT_DATE)
);

-- Issue history table with foreign key constraints
CREATE TABLE issue_history (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE NOT NULL,
    actual_return_date DATE NULL,
    fine INT DEFAULT 0,
    status ENUM('issued', 'returned') DEFAULT 'issued',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

-- Insert sample users with Indian names
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('rajesh_librarian', 'raj123', 'admin'),
('arjun_student', 'arjun123', 'user'),
('priya_sharma', 'priya456', 'user'),
('rohit_kumar', 'rohit789', 'user'),
('kavya_patel', 'kavya321', 'user');

-- Insert sample books with Indian authors and relevant titles
INSERT INTO books (name, author, total, available) VALUES
('Gitanjali', 'Rabindranath Tagore', 5, 4),
('The God of Small Things', 'Arundhati Roy', 4, 2),
('Midnight Children', 'Salman Rushdie', 3, 3),
('A Fine Balance', 'Rohinton Mistry', 6, 5),
('Train to Pakistan', 'Khushwant Singh', 4, 3),
('Wings of Fire', 'A. P. J. Abdul Kalam', 8, 6),
('My Experiments with Truth', 'Mahatma Gandhi', 5, 4),
('Discovery of India', 'Jawaharlal Nehru', 3, 2),
('Ramayana', 'Valmiki', 7, 6),
('Mahabharata', 'Vyasa', 4, 3),
('Shantaram', 'Gregory David Roberts', 2, 1),
('Sacred Games', 'Vikram Chandra', 5, 4),
('The White Tiger', 'Aravind Adiga', 3, 2),
('Kamala Das Poems', 'Kamala Das', 4, 4),
('Godan', 'Munshi Premchand', 6, 5);

-- Insert sample students with Indian names and details
INSERT INTO students (name, email, phone) VALUES
('Aarav Sharma', 'aarav.sharma@gmail.com', '9876543210'),
('Diya Patel', 'diya.patel@yahoo.in', '9876543211'),
('Arjun Kumar', 'arjun.kumar@gmail.com', '9876543212'),
('Kavya Singh', 'kavya.singh@outlook.com', '9876543213'),
('Rohit Mehta', 'rohit.mehta@gmail.com', '9876543214'),
('Ananya Gupta', 'ananya.gupta@rediffmail.com', '9876543215'),
('Ishaan Joshi', 'ishaan.joshi@gmail.com', '9876543216'),
('Priya Reddy', 'priya.reddy@hotmail.com', '9876543217'),
('Vikram Agarwal', 'vikram.agarwal@gmail.com', '9876543218'),
('Shreya Mishra', 'shreya.mishra@yahoo.in', '9876543219'),
('Karan Verma', 'karan.verma@gmail.com', '9876543220'),
('Riya Khanna', 'riya.khanna@outlook.com', '9876543221');

-- Insert sample issue history with Indian context
INSERT INTO issue_history (student_id, book_id, issue_date, return_date, actual_return_date, fine, status) VALUES
(1, 1, '2025-09-01', '2025-09-15', '2025-09-14', 0, 'returned'),
(2, 6, '2025-09-05', '2025-09-19', '2025-09-22', 15, 'returned'),
(3, 9, '2025-09-10', '2025-09-24', NULL, 0, 'issued'),
(4, 2, '2025-09-12', '2025-09-26', '2025-09-25', 0, 'returned'),
(5, 7, '2025-09-15', '2025-09-29', NULL, 0, 'issued'),
(6, 10, '2025-09-18', '2025-10-02', NULL, 0, 'issued'),
(7, 12, '2025-09-20', '2025-10-04', NULL, 0, 'issued'),
(8, 3, '2025-08-25', '2025-09-08', '2025-09-12', 20, 'returned'),
(9, 13, '2025-09-22', '2025-10-06', NULL, 0, 'issued'),
(10, 5, '2025-09-23', '2025-10-07', NULL, 0, 'issued'),
(11, 8, '2025-09-20', '2025-10-04', '2025-09-28', 0, 'returned'),
(12, 14, '2025-09-18', '2025-10-02', NULL, 0, 'issued'),
(1, 15, '2025-09-25', '2025-10-09', NULL, 0, 'issued');
