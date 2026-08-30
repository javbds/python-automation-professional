Production Health Automation
-Configuring what the system checks
-Checks what system youre using
-Determines the health status of monitored components
-If the external API is healthy to utilize the task
-Checks temporary failed requests 
-generate a human readable health report
-Log any INFO, WARNINGS, ERRORS, SUCCESSESS


Inputs
-Server(s) names(s)
-What processes to moniter
-API URL
-Limited requests before timeout
-MAX retry attempts

Outputs
-A human understandable report
-Includes:
    Server, System, Process, API, Attempts, and Overall status

Failure Cases
-Process: exists? running? valid?
-API: Error Codes, Timeouts, Connection, Valid?
-Config: Missing, empty, invalid values; timeout, retry count valid?

Components
get_config
validate_config
get_system_info
check_process
check_api_health
build_report
print_health_report
main

Testing Targets
valid configuration
invalid configuration
system information returned
process running
process not running
API success
API retry then success
API retry exhaustion
permanent API failure
report construction
