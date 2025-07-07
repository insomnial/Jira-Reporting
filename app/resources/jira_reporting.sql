--
-- Table structure for table `layout`
--
CREATE TABLE `layout` (
  `id` int PRIMARY KEY,
  `table` tinytext NOT NULL
);
INSERT INTO `layout` (`id`, `table`) VALUES (NULL, 'status');
INSERT INTO `layout` (`id`, `table`) VALUES (NULL, 'workitem_changelog');
INSERT INTO `layout` (`id`, `table`) VALUES (NULL, 'workitem_detail');
--
-- Table structure for table `status`
--
CREATE TABLE `status` (
  `id` int PRIMARY KEY,
  `project` tinytext NOT NULL,
  `label` tinytext NOT NULL,
  `identifier` tinytext NOT NULL
);
--
-- Table structure for table `workitem_changelog`
--
CREATE TABLE `workitem_changelog` (
  `id` int PRIMARY KEY,
  `atlassian_keyid` tinytext NOT NULL,
  `datetime` datetime NOT NULL,
  `event` tinytext NOT NULL
);
--
-- Table structure for table `workitem_detail`
--
CREATE TABLE `workitem_detail` (
  `id` int PRIMARY KEY,
  `atlassian_keyid` tinytext NOT NULL,
  `assignee` tinytext NOT NULL,
  `reporter` tinytext NOT NULL,
  `summary` tinytext NOT NULL,
  `updated` tinytext NOT NULL,
  `priority` int NOT NULL,
  `status` int NOT NULL,
  `created` datetime NOT NULL,
  `issue_type` tinytext NOT NULL,
  `request_type` tinytext NOT NULL
);
