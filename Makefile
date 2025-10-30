.PHONY: crawl promote web-dev

crawl:
	cd crawler && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && python run_all.py --regions "GA,Grand Rapids, MI, West Michigan"

promote:
	cd crawler && . .venv/bin/activate && python promote_submissions.py --limit 20

web-dev:
	cd web && npm i && npm run dev
