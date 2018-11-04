-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 04, 2018 at 05:35 PM
-- Server version: 10.1.35-MariaDB
-- PHP Version: 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cen`
--

-- --------------------------------------------------------

--
-- Table structure for table `comment_cab`
--

CREATE TABLE `comment_cab` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `cab_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comment_cab`
--

INSERT INTO `comment_cab` (`id`, `username`, `cab_id`, `text`, `timestamp`, `user_id`) VALUES
(2, 'atapi', 1, 'daadsdada', '2018-11-03 15:56:13', 1),
(3, 'vinit1', 3, 'saasda', '2018-11-03 16:55:30', 3),
(4, 'vinit1', 1, 'dsaddas', '2018-11-03 16:56:42', 3);

-- --------------------------------------------------------

--
-- Table structure for table `comment_post`
--

CREATE TABLE `comment_post` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `post_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comment_post`
--

INSERT INTO `comment_post` (`id`, `username`, `post_id`, `text`, `timestamp`, `user_id`) VALUES
(5, 'atapi', 3, 'caccmakl 1 ', '2018-11-01 21:27:32', 1),
(6, 'atapi', 5, 'kafsfsjk', '2018-11-01 21:44:17', 1),
(7, 'vinit1', 3, 'pls sell', '2018-11-01 22:00:25', 3),
(8, 'unique', 5, 'pls sell to me \r\ni ruski ', '2018-11-01 22:14:53', 5),
(13, 'rock', 8, 'rocker', '2018-11-03 15:46:24', 7),
(14, 'rock', 6, 'rock', '2018-11-03 15:46:33', 7),
(15, 'vinit1', 6, 'vvvvv', '2018-11-03 16:48:09', 3),
(16, 'vinit1', 6, 'fsdsdfds', '2018-11-03 16:48:48', 3),
(17, 'vinit1', 6, 'vghgfg', '2018-11-03 16:51:35', 3),
(18, 'atapi', 6, 'asdf asdf\r\n', '2018-11-04 16:26:28', 1);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `username` varchar(11) NOT NULL,
  `text` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `link` text NOT NULL,
  `seen` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `username`, `text`, `timestamp`, `link`, `seen`) VALUES
(2, 'atapi', 'Comment on Computer by vinit1', '2018-11-03 16:52:06', '/post_details/6', 0),
(3, 'atapi', 'Comment on Computer by atapi', '2018-11-03 16:52:03', '/post_details/6', 0),
(4, 'atapi', 'Comment on Cab Sharing from kgptohorah on 2018-10-01 by vinit1', '2018-11-03 16:56:42', '/cab_details/1', 0),
(5, 'atapi', 'Comment on Item Computer by atapi', '2018-11-04 16:26:28', '/post_details/6', 0);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(30) NOT NULL,
  `description` text NOT NULL,
  `price` int(11) NOT NULL,
  `image_path` varchar(50) NOT NULL,
  `sold` tinyint(1) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `category` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `username`, `user_id`, `title`, `description`, `price`, `image_path`, `sold`, `timestamp`, `category`) VALUES
(6, 'atapi', 1, 'Computer', 'adsdsadsasa', 1122, 'uploadedimages/coins_1.jpg', 0, '2018-11-03 14:18:45', 'Electronics'),
(7, 'atapi', 1, 'Bike', 'asdadsdfdsdsdsdsf', 33000, 'uploadedimages/thumb-1920-577286.png', 0, '2018-11-03 14:18:56', 'Bikes'),
(8, 'vinit1', 3, 'rocket', 'v2', 1, 'uploadedimages/coins.jpg', 0, '2018-11-03 14:19:06', 'Others'),
(9, 'atapi', 1, 'car Audi', 'Audi R8 ', 99999, 'uploadedimages/received_377685415917145_2.jpeg', 0, '2018-11-03 14:18:20', 'Cars'),
(10, 'atapi', 1, 'car', 'hfghhr rgerrh rheh', 10000, 'uploadedimages/received_377685415917145_3.jpeg', 0, '2018-11-04 16:29:56', 'Cars');

-- --------------------------------------------------------

--
-- Table structure for table `sharing`
--

CREATE TABLE `sharing` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `seats` int(11) NOT NULL,
  `source` varchar(30) NOT NULL,
  `destination` varchar(30) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sharing`
--

INSERT INTO `sharing` (`id`, `username`, `user_id`, `date`, `time`, `seats`, `source`, `destination`, `price`) VALUES
(1, 'atapi', 1, '2018-10-01', '01:01:00', 2, 'kgp', 'horah', 213),
(3, 'vinit1', 3, '2018-11-30', '19:30:00', 2, 'kgp', 'sonaghachi', 400);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(40) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `phone_number` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `name`, `email`, `username`, `password`, `phone_number`) VALUES
(1, 'atapi prasad', 'atapi@gmail.com', 'atapi', 'atapi', '9950251130'),
(3, 'Vinit', 'vinitkumawat31@gmail.com', 'vinit1', 'vinit', '9950251131'),
(4, 'user3', 'user3@gmail.com', 'user3', 'user3', '09950251130'),
(5, 'krishna', 'krishna@gmail.com', 'unique', '123', '09950251122'),
(6, 'vx', 'vx@gamil.com', 'vx', 'llolol', '09950251131'),
(7, 'rock', 'rock@gmail.com', 'rock', 'rock', '1234567890');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comment_cab`
--
ALTER TABLE `comment_cab`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `comment_post`
--
ALTER TABLE `comment_post`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sharing`
--
ALTER TABLE `sharing`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comment_cab`
--
ALTER TABLE `comment_cab`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `comment_post`
--
ALTER TABLE `comment_post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `sharing`
--
ALTER TABLE `sharing`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_pk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
