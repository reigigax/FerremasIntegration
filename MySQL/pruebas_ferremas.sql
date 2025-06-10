-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-06-2025 a las 01:16:38
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pruebas_ferremas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `codigo_producto` varchar(8) NOT NULL,
  `marca_producto` varchar(30) NOT NULL,
  `nombre_producto` varchar(30) NOT NULL,
  `categoria_producto` varchar(30) NOT NULL,
  `stock` int(11) NOT NULL,
  `sucursal` varchar(30) NOT NULL,
  `valor` float NOT NULL,
  `descripcion` varchar(150) DEFAULT NULL,
  `img_producto` varchar(400) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `codigo_producto`, `marca_producto`, `nombre_producto`, `categoria_producto`, `stock`, `sucursal`, `valor`, `descripcion`, `img_producto`) VALUES
(1, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 36, 'CACFerremasSTGO01', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375'),
(2, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 19, 'CACFerremasSTGO02', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375'),
(3, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 25, 'CPSFerremasSTGO03', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375'),
(4, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 10, 'MiniCACFerremasSTGO04', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375'),
(5, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 0, 'CACFerremasREGIONES05', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375'),
(6, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 6, 'CPSFerremasREGIONES06', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375'),
(7, 'SKU14923', 'TGO', 'MARTILLO CARPINTERO 500GR', 'Herramientas Manuales', 1, 'MiniCACFerremasREGIONES07', 3990, 'Tipo: Martillo Carpintero, Peso: 500GR, Tamaño Total: 33 x 14 x 3cm, Mango Antideslizante', 'https://cdnx.jumpseller.com/almasolar-cl/image/42443491/resize/640/640?1700600375');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
