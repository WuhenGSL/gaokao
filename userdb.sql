/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80100 (8.1.0)
 Source Host           : localhost:3306
 Source Schema         : userdb

 Target Server Type    : MySQL
 Target Server Version : 80100 (8.1.0)
 File Encoding         : 65001

 Date: 27/07/2023 16:04:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `score` int NOT NULL,
  `rank` int NOT NULL,
  `subject1` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `subject2` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `subject3` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` (`name`, `password`, `email`, `score`, `rank`, `subject1`, `subject2`, `subject3`) VALUES ('admin', '123', 'admin@admin.com', 590, 5000, '物理', '化学', '生物');
INSERT INTO `user` (`name`, `password`, `email`, `score`, `rank`, `subject1`, `subject2`, `subject3`) VALUES ('wuhen', '123', 'wuhen@qq.com', 601, 10000, '物理', '政治', '生物');
COMMIT;

-- ----------------------------
-- Table structure for userselection
-- ----------------------------
DROP TABLE IF EXISTS `userselection`;
CREATE TABLE `userselection` (
  `id` int NOT NULL,
  `school` varchar(254) DEFAULT NULL,
  `specialty` varchar(254) DEFAULT NULL,
  `lowest_rank` int DEFAULT NULL,
  `feature` varchar(254) DEFAULT NULL,
  `probability` int DEFAULT NULL,
  `name` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of userselection
-- ----------------------------
BEGIN;
INSERT INTO `userselection` (`id`, `school`, `specialty`, `lowest_rank`, `feature`, `probability`, `name`) VALUES (1, '北京邮电大学', '电子信息类', 4096, '公办本科 · 211 双一流 教育部直属', 14, 'admin');
INSERT INTO `userselection` (`id`, `school`, `specialty`, `lowest_rank`, `feature`, `probability`, `name`) VALUES (2, '大连理工大学', '电子信息类(创新班)', 4677, '公办本科 · 985 211 双一流 教育部直属 强基计划', 38, 'admin');
INSERT INTO `userselection` (`id`, `school`, `specialty`, `lowest_rank`, `feature`, `probability`, `name`) VALUES (3, '西北工业大学', '电子信息类', 4319, '公办本科 · 985 211 双一流 中央部委院 强基计划', 23, 'admin');
INSERT INTO `userselection` (`id`, `school`, `specialty`, `lowest_rank`, `feature`, `probability`, `name`) VALUES (4, '华南理工大学', '电气类', 4571, '公办本科 · 985 211 双一流 教育部直属 强基计划', 33, 'admin');
INSERT INTO `userselection` (`id`, `school`, `specialty`, `lowest_rank`, `feature`, `probability`, `name`) VALUES (5, '四川大学', '电气类', 5667, '公办本科 · 985 211 双一流 教育部直属 强基计划', 64, 'admin');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
