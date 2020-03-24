SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tbl_opinion
-- ----------------------------
DROP TABLE IF EXISTS `tbl_opinion`;
CREATE TABLE `tbl_opinion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(1000) DEFAULT '',
  `key_word` varchar(50) DEFAULT NULL,
  `url` varchar(500) DEFAULT '',
  `content` text DEFAULT NULL,
  `degist` varchar(500) DEFAULT NULL,
  `publish_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `source` varchar(50) DEFAULT NULL,
  `author` varchar(50) DEFAULT NULL,
  `tenden` tinyint(4) DEFAULT NULL COMMENT '0：负面；1：中性；2：正面',
  `media_id` bigint(20) DEFAULT NULL COMMENT '0：媒体；1：论坛；2：微博；3：微信；4：博客；5：报刊；6：视频；7：APP；\r\n            8：其它；9：评论\r\n            ',
  `level` varchar(50) DEFAULT NULL,
  `area_id` bigint(20) DEFAULT NULL,
  `comment` int(11) DEFAULT 0 COMMENT '评论数',
  `read` int(11) DEFAULT 0 COMMENT '阅读数',
  `like` int(11) DEFAULT 0 COMMENT '点赞数',
  `transpond` int(11) DEFAULT 0 COMMENT '转发数',
  `digest_id` bigint(20) DEFAULT NULL,
  `data_id` bigint(20) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `tenden_state` tinyint(4) DEFAULT 0 COMMENT '0：待分析；1：分析中；2：已完成',
  `topic_status` tinyint(4) DEFAULT 5 COMMENT '话题状态(1置顶，2精选，3热门，4普通，5默认)',
  PRIMARY KEY (`id`),
  KEY `idindex` (`id`),
  KEY `titleindex` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=1086578 DEFAULT CHARSET=utf8 MAX_ROWS=1000000000;

-- ----------------------------
-- Table structure for tbl_data_resource
-- ----------------------------

CREATE TABLE `tbl_data_resource` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `media_id` bigint(20) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `url` varchar(100) DEFAULT NULL,
  `area_id` bigint(20) DEFAULT NULL,
  `level` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34986 DEFAULT CHARSET=utf8
