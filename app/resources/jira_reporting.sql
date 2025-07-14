--
-- Table structure for table 'metadata'
--
CREATE TABLE `metadata` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `open_timestamp` timestamp NOT NULL
);
--
-- Table structure for table `layout`
--
CREATE TABLE `layout` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `table` tinytext NOT NULL
);
INSERT INTO `layout` (`id`, `table`) VALUES (NULL, 'status');
INSERT INTO `layout` (`id`, `table`) VALUES (NULL, 'workitem_changelog');
INSERT INTO `layout` (`id`, `table`) VALUES (NULL, 'workitem_detail');
--
-- Table structure for table `status`
--
CREATE TABLE `status` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `project` tinytext NOT NULL,
  `label` tinytext NOT NULL,
  `identifier` tinytext NOT NULL
);
--
-- Table structure for table `workitem_changelog`
--
CREATE TABLE `workitem_changelog` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `keyid` tinytext NOT NULL,
  `datetime` datetime NOT NULL,
  `event` tinytext NOT NULL
);
--
-- Table structure for table `workitem_detail`
--
CREATE TABLE `workitem_detail` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `key` tinytext NOT NULL,
  `assignee` tinytext NOT NULL,
  `reporter` tinytext NOT NULL,
  `summary` tinytext NOT NULL,
  `updated` tinytext NOT NULL,
  `priority` tinytext NOT NULL,
  `status` tinytext NOT NULL,
  `created` tinytext NOT NULL,
  `issue_type` tinytext NOT NULL,
  `request_type` tinytext NOT NULL,
  `details` json NOT NULL
);
