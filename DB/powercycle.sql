-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 08, 2026 at 12:52 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `powercycle`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `CategoryID` int(11) NOT NULL,
  `CategoryName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`CategoryID`, `CategoryName`) VALUES
(1, 'Mobile Phones'),
(2, 'Smartphones'),
(3, 'Tablets'),
(4, 'Laptops'),
(5, 'Desktop Computers'),
(6, 'Computer Components'),
(7, 'Monitors'),
(8, 'Keyboards & Mice'),
(9, 'Printers & Scanners'),
(10, 'Computer Accessories'),
(11, 'Audio Devices'),
(12, 'Headphones & Earphones'),
(13, 'Speakers'),
(14, 'Microphones'),
(15, 'Cameras'),
(16, 'DSLR & Mirrorless Cameras'),
(17, 'Action Cameras'),
(18, 'Camera Lenses'),
(19, 'Camera Accessories'),
(20, 'Gaming Consoles'),
(21, 'Video Games'),
(22, 'Game Controllers'),
(23, 'Gaming Accessories'),
(24, 'Smart TVs'),
(25, 'Televisions'),
(26, 'Projectors'),
(27, 'Streaming Devices'),
(28, 'Smartwatches'),
(29, 'Wearable Technology'),
(30, 'Fitness Trackers'),
(31, 'Networking Devices'),
(32, 'Routers & Modems'),
(33, 'WiFi Extenders'),
(34, 'Network Switches'),
(35, 'Storage Devices'),
(36, 'External Hard Drives'),
(37, 'USB Flash Drives'),
(38, 'Memory Cards'),
(39, 'Home Electronics'),
(40, 'Smart Home Devices'),
(41, 'Security Cameras'),
(42, 'IoT Devices'),
(43, 'Electronic Accessories'),
(44, 'Chargers & Cables'),
(45, 'Power Banks'),
(46, 'Adapters'),
(47, 'Other Electronics');

-- --------------------------------------------------------

--
-- Table structure for table `listing`
--

CREATE TABLE `listing` (
  `ListingID` int(11) NOT NULL,
  `SellerID` int(11) NOT NULL,
  `CategoryID` int(11) NOT NULL,
  `ListingTitle` varchar(255) NOT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Condition` varchar(100) DEFAULT NULL,
  `Price` decimal(10,2) NOT NULL,
  `ListingDescription` text DEFAULT NULL,
  `item_count` int(11) DEFAULT 0,
  `Created_at` datetime NOT NULL,
  `Updated_at` datetime DEFAULT NULL,
  `isCurrent` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `listing`
--

INSERT INTO `listing` (`ListingID`, `SellerID`, `CategoryID`, `ListingTitle`, `Location`, `Condition`, `Price`, `ListingDescription`, `item_count`, `Created_at`, `Updated_at`, `isCurrent`) VALUES
(11, 19, 4, 'Laptop', 'pangasinan', 'Brand New', 1256.00, 'brand new', 0, '2026-01-08 04:54:29', NULL, 1),
(12, 21, 1, 'Cellphone', 'Urdaneta', 'Brand New', 1264.00, 'nahulog', 1, '2026-01-08 05:22:04', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `listing_image`
--

CREATE TABLE `listing_image` (
  `ImageID` int(11) NOT NULL,
  `ListingID` int(11) NOT NULL,
  `ImagePath` varchar(255) NOT NULL,
  `isPrimary` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `listing_image`
--

INSERT INTO `listing_image` (`ImageID`, `ListingID`, `ImagePath`, `isPrimary`) VALUES
(24, 11, '11_0_608674658_26207192012218556_822060125296242889_n.jpg', 1),
(25, 11, '11_1_576932601_122148741470702036_506139493031589090_n.jpg', 0),
(26, 11, '11_2_470525320_1577849296439240_8379310426704942006_n.jpg', 0),
(27, 11, '11_3_607559577_857808063802758_349684145700567378_n.jpg', 0),
(28, 11, '11_4_605238579_2202030256994593_4499822406646950990_n.png', 0),
(29, 11, '11_5_423fcfc4-9ff4-4ff8-82d4-32b67db703bd_1.png', 0),
(30, 11, '11_6_423fcfc4-9ff4-4ff8-82d4-32b67db703bd.png', 0),
(31, 11, '11_7_601758478_735513349605390_7966509263152298891_n.png', 0),
(32, 11, '11_8_pexels-falling4utah-2724748.jpg', 0),
(33, 12, '12_0_608674658_26207192012218556_822060125296242889_n.jpg', 1),
(34, 12, '12_1_576932601_122148741470702036_506139493031589090_n.jpg', 0),
(35, 12, '12_2_470525320_1577849296439240_8379310426704942006_n.jpg', 0),
(36, 12, '12_3_607559577_857808063802758_349684145700567378_n.jpg', 0),
(37, 12, '12_4_605238579_2202030256994593_4499822406646950990_n.png', 0),
(38, 12, '12_5_598778911_1297283202156857_6466906564891005404_n.png', 0),
(39, 12, '12_6_423fcfc4-9ff4-4ff8-82d4-32b67db703bd_1.png', 0),
(40, 12, '12_7_423fcfc4-9ff4-4ff8-82d4-32b67db703bd.png', 0),
(41, 12, '12_8_601758478_735513349605390_7966509263152298891_n.png', 0),
(42, 12, '12_9_pexels-falling4utah-2724748.jpg', 0);

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `OrderID` int(11) NOT NULL,
  `BuyerID` int(11) NOT NULL,
  `TotalAmount` decimal(10,2) NOT NULL,
  `isCurrent` tinyint(1) DEFAULT 1,
  `Created_at` datetime DEFAULT current_timestamp(),
  `Updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`OrderID`, `BuyerID`, `TotalAmount`, `isCurrent`, `Created_at`, `Updated_at`) VALUES
(5, 20, 1256.00, 1, '2026-01-08 05:18:12', NULL),
(6, 20, 1264.00, 0, '2026-01-08 05:22:34', '2026-01-08 05:22:36'),
(7, 20, 1264.00, 1, '2026-01-08 05:31:05', NULL),
(8, 5, 6845.00, 1, '2026-01-08 07:22:27', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `orderitem`
--

CREATE TABLE `orderitem` (
  `OrderItemID` int(11) NOT NULL,
  `OrderID` int(11) NOT NULL,
  `ListingID` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderitem`
--

INSERT INTO `orderitem` (`OrderItemID`, `OrderID`, `ListingID`, `Quantity`) VALUES
(5, 5, 11, 1),
(6, 6, 12, 1),
(7, 7, 12, 1);

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `TransactionID` int(11) NOT NULL,
  `OrderID` int(11) NOT NULL,
  `TransactionStatus` enum('Pending','Completed','Cancelled') DEFAULT 'Pending',
  `BuyerConfirmed` tinyint(1) DEFAULT 0,
  `SellerConfirmed` tinyint(1) DEFAULT 0,
  `Created_at` datetime DEFAULT current_timestamp(),
  `Updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`TransactionID`, `OrderID`, `TransactionStatus`, `BuyerConfirmed`, `SellerConfirmed`, `Created_at`, `Updated_at`) VALUES
(5, 5, 'Completed', 1, 1, '2026-01-08 05:18:12', '2026-01-08 05:18:56'),
(6, 6, 'Cancelled', 0, 0, '2026-01-08 05:22:34', '2026-01-08 05:28:52'),
(7, 7, 'Cancelled', 1, 0, '2026-01-08 05:31:05', '2026-01-08 05:45:30'),
(8, 8, 'Cancelled', 0, 0, '2026-01-08 07:22:27', '2026-01-08 07:22:35');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `UserID` int(11) NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `UserType` enum('Buyer','Seller','Admin') NOT NULL DEFAULT 'Buyer',
  `isCurrent` tinyint(1) DEFAULT 1,
  `Created_at` datetime DEFAULT current_timestamp(),
  `Updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`UserID`, `FirstName`, `LastName`, `Email`, `Password`, `UserType`, `isCurrent`, `Created_at`, `Updated_at`) VALUES
(5, 'Admin', 'User', 'admin@powercycle.com', 'admin123', 'Admin', 1, '2026-01-07 18:52:07', NULL),
(19, 'Buyer', 'makk', 'makmak@powercycle.com', '123456', 'Seller', 1, '2026-01-08 03:20:33', NULL),
(20, 'Makmaks', 'Aban', 'makmaks@powercycle.com', '123456', 'Buyer', 1, '2026-01-08 05:18:04', NULL),
(21, 'seller', 'one', 'seller1@gmail.com', '123456789', 'Seller', 1, '2026-01-08 05:20:54', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`CategoryID`);

--
-- Indexes for table `listing`
--
ALTER TABLE `listing`
  ADD PRIMARY KEY (`ListingID`),
  ADD KEY `CategoryID` (`CategoryID`),
  ADD KEY `fk_listing_user` (`SellerID`);

--
-- Indexes for table `listing_image`
--
ALTER TABLE `listing_image`
  ADD PRIMARY KEY (`ImageID`),
  ADD KEY `fk_listing_image` (`ListingID`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `fk_order_buyer` (`BuyerID`);

--
-- Indexes for table `orderitem`
--
ALTER TABLE `orderitem`
  ADD PRIMARY KEY (`OrderItemID`),
  ADD KEY `fk_orderitem_order` (`OrderID`),
  ADD KEY `fk_orderitem_listing` (`ListingID`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `fk_transaction_order` (`OrderID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `CategoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `listing`
--
ALTER TABLE `listing`
  MODIFY `ListingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `listing_image`
--
ALTER TABLE `listing_image`
  MODIFY `ImageID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `orderitem`
--
ALTER TABLE `orderitem`
  MODIFY `OrderItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `TransactionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `listing`
--
ALTER TABLE `listing`
  ADD CONSTRAINT `fk_listing_user` FOREIGN KEY (`SellerID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE,
  ADD CONSTRAINT `listing_ibfk_2` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`);

--
-- Constraints for table `listing_image`
--
ALTER TABLE `listing_image`
  ADD CONSTRAINT `fk_listing_image` FOREIGN KEY (`ListingID`) REFERENCES `listing` (`ListingID`) ON DELETE CASCADE;

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `fk_order_buyer` FOREIGN KEY (`BuyerID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE;

--
-- Constraints for table `orderitem`
--
ALTER TABLE `orderitem`
  ADD CONSTRAINT `fk_orderitem_listing` FOREIGN KEY (`ListingID`) REFERENCES `listing` (`ListingID`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_orderitem_order` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`) ON DELETE CASCADE,
  ADD CONSTRAINT `orderitem_ibfk_2` FOREIGN KEY (`ListingID`) REFERENCES `listing` (`ListingID`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `fk_transaction_order` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
