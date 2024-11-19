-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-03-2022 a las 20:59:46
-- Versión del servidor: 10.4.19-MariaDB
-- Versión de PHP: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tallercompu`
--
CREATE DATABASE IF NOT EXISTS `tallercompu` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `tallercompu`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargador`
--

CREATE TABLE `cargador` (
  `serial_cargador` varchar(18) NOT NULL,
  `marca_cargador` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cargador`
--

INSERT INTO `cargador` (`serial_cargador`, `marca_cargador`) VALUES
('55677', 'acer');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `cedula` varchar(16) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `correo` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`cedula`, `nombre`, `apellido`, `direccion`, `telefono`, `correo`) VALUES
('345677', 'homero simpson', 'simpson', 'avenida siempre viva', '789-345', 'bart@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dispositivo`
--

CREATE TABLE `dispositivo` (
  `serial_dispositivo` varchar(50) NOT NULL,
  `marca` varchar(30) NOT NULL,
  `tipo` varchar(30) NOT NULL,
  `dispositivo_cargador` varchar(18) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `dispositivo`
--

INSERT INTO `dispositivo` (`serial_dispositivo`, `marca`, `tipo`, `dispositivo_cargador`) VALUES
('7433233', 'acer', 'portatil', '55677');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `id_factura` int(11) NOT NULL,
  `fecha_factura` datetime NOT NULL,
  `cliente_factura` varchar(16) DEFAULT NULL,
  `dispositivo_factura` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparacion`
--

CREATE TABLE `reparacion` (
  `id_reparacion` int(11) NOT NULL,
  `detalles` varchar(500) NOT NULL,
  `dispositivo_reparacion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `reparacion`
--

INSERT INTO `reparacion` (`id_reparacion`, `detalles`, `dispositivo_reparacion`) VALUES
(10012, 'cambio de pantalla', '7433233');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cargador`
--
ALTER TABLE `cargador`
  ADD PRIMARY KEY (`serial_cargador`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`cedula`);

--
-- Indices de la tabla `dispositivo`
--
ALTER TABLE `dispositivo`
  ADD PRIMARY KEY (`serial_dispositivo`),
  ADD KEY `dispositivo_cargador` (`dispositivo_cargador`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`id_factura`),
  ADD KEY `cliente_factura` (`cliente_factura`),
  ADD KEY `dispositivo_factura` (`dispositivo_factura`);

--
-- Indices de la tabla `reparacion`
--
ALTER TABLE `reparacion`
  ADD PRIMARY KEY (`id_reparacion`),
  ADD KEY `dispositivo_reparacion` (`dispositivo_reparacion`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `id_factura` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reparacion`
--
ALTER TABLE `reparacion`
  MODIFY `id_reparacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10013;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `dispositivo`
--
ALTER TABLE `dispositivo`
  ADD CONSTRAINT `dispositivo_ibfk_1` FOREIGN KEY (`dispositivo_cargador`) REFERENCES `cargador` (`serial_cargador`);

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`cliente_factura`) REFERENCES `cliente` (`cedula`),
  ADD CONSTRAINT `factura_ibfk_2` FOREIGN KEY (`dispositivo_factura`) REFERENCES `dispositivo` (`serial_dispositivo`);

--
-- Filtros para la tabla `reparacion`
--
ALTER TABLE `reparacion`
  ADD CONSTRAINT `reparacion_ibfk_1` FOREIGN KEY (`dispositivo_reparacion`) REFERENCES `dispositivo` (`serial_dispositivo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
