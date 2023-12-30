-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Okt 2023 pada 15.57
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uts_kelompok6_carrental`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `data_mobil`
--

CREATE TABLE `data_mobil` (
  `id_mobil` int(10) NOT NULL,
  `gambar` text NOT NULL,
  `nama_mobil` varchar(100) NOT NULL,
  `brand_mobil` varchar(100) NOT NULL,
  `kilometer` int(100) NOT NULL,
  `transmisi` enum('Manual','Matic','Hybrid') NOT NULL,
  `kapasitas_mobil` enum('4 Seat','6 Seat') NOT NULL,
  `jenis_bensin` enum('Pertalite','Pertamax','Solar') NOT NULL,
  `harga` int(11) NOT NULL,
  `deskripsi` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `data_mobil`
--

INSERT INTO `data_mobil` (`id_mobil`, `gambar`, `nama_mobil`, `brand_mobil`, `kilometer`, `transmisi`, `kapasitas_mobil`, `jenis_bensin`, `harga`, `deskripsi`) VALUES
(1, 'crv.jpg', 'CR-V', 'Honda', 1000, 'Matic', '6 Seat', 'Pertamax', 900000, 'Jadilah yang terdepan dengan SUV andalan terbaru dari Honda, All New Honda CR-V yang kini hadir dalam pilihan mesin hybrid untuk konsumsi bahan bakar lebih hemat dan tenaga powerful.'),
(2, 'hyundai.jpg', 'Palisade', 'Hyundai', 5000, 'Matic', '6 Seat', 'Pertamax', 1000000, 'The bold, premium look of the new PALISADE commands immediate attention wherever your travels take you.\r\nIt’s a unique look that inspires confident driving and your confidence is well placed: PALISADE’s advanced\r\nsafety features keep you and your loved ones free from danger. PALISADE’s spacious cabin, flexible seating,\r\nand advanced connectivity features make it the perfect getaway family car.'),
(3, 'Xpander.png', 'Xpander Ultimate', 'Mitsubishi', 2000, 'Matic', '6 Seat', 'Pertamax', 800000, 'Ini adalah mobil Xpander keren masih fresh takda cacat. '),
(4, 'yaris.jpeg', 'yaris', 'totoyoyotata', 16050494, 'Manual', '4 Seat', 'Pertalite', 150000, 'pink pig '),
(5, 'EVO-5-yellow.jpg', 'Lancer Evolution VI', 'Mitsubishi', 9000, 'Manual', '4 Seat', 'Pertamax', 2147483647, 'gud car yes'),
(6, 'image_2023-10-23_230024250.png', 'Retro costume', 'Elegy', 802000000, 'Manual', '4 Seat', 'Pertamax', 2147483647, 'mint condition'),
(7, 'image_2023-10-23_230252225.png', 'FW42', 'Williams', 80, 'Manual', '4 Seat', 'Pertamax', 90000000, 'tidak termasuk orang terpisah'),
(8, 'image_2023-10-23_230429360.png', 'Mercedes Benz 770', 'Mercedes Benz', 998, 'Manual', '6 Seat', 'Pertamax', 800000022, 'punya orang jerman'),
(9, 'image_2023-10-23_230522347.png', 'avanza', 'totoyoyotata', 7500, 'Hybrid', '6 Seat', 'Pertalite', 65000, 'masih muus '),
(10, 'image_2023-10-23_230651213.png', 'XJ220', 'Jaguar', 900000, 'Manual', '4 Seat', 'Pertamax', 75000000, 'masih mulus'),
(11, 'image_2023-10-23_230754305.png', 'M4 1999', 'BMW', 32154213, 'Manual', '4 Seat', 'Pertamax', 2147483647, 'masih mulus'),
(12, 'image_2023-10-23_230853022.png', 'GOLF GTI', 'Volkswagen', 2193823, 'Manual', '4 Seat', 'Pertamax', 2147483647, 'masih mulus :)');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `data_mobil`
--
ALTER TABLE `data_mobil`
  ADD PRIMARY KEY (`id_mobil`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `data_mobil`
--
ALTER TABLE `data_mobil`
  MODIFY `id_mobil` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
