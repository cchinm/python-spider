[TOC]

# bililive-哔哩哔哩直播房间数据收集

前期准备

    执行SQL
    
    CREATE TABLE `bili_live_data`  (
      `area_id` int(11) DEFAULT NULL,
      `parea_id` int(11) DEFAULT NULL,
      `amo` int(11) DEFAULT NULL,
      `sum` int(11) DEFAULT NULL,
      `total` int(11) DEFAULT NULL,
      `pages` int(11) DEFAULT 1,
      `female` int(11) DEFAULT 0,
      `male` int(11) DEFAULT 0,
      `ctime` datetime(0) DEFAULT NULL,
      `update_time` timestamp(0) DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
      `max_hour` int(2) DEFAULT 0,
      `avg_hour` int(2) DEFAULT 0,
      UNIQUE INDEX `key`(`area_id`, `parea_id`, `ctime`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
    ------------------------------
    DROP TABLE IF EXISTS `bili_live_room`;
    CREATE TABLE `bili_live_room`  (
      `area_id` int(11) NOT NULL,
      `room_id` int(11) DEFAULT NULL,
      `parea_id` int(11) DEFAULT NULL,
      `ctime` datetime(0) DEFAULT NULL,
      `id` int(11) NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE INDEX `key`(`room_id`, `ctime`) USING BTREE,
      INDEX `k_area_id`(`area_id`, `parea_id`) USING BTREE
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
    
    -----------------
    DROP TABLE IF EXISTS `bili_room_info`;
    CREATE TABLE `bili_room_info`  (
      `room_id` int(11) DEFAULT NULL,
      `gender` int(1) DEFAULT NULL,
      `uid` int(11) DEFAULT NULL,
      `create_time` datetime(0) DEFAULT NULL,
      UNIQUE INDEX `key1`(`room_id`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
    
执行说明
    
    scrapy crawl bililive
    
# pybrowser

    Just searching something with Python in Sogo.
    