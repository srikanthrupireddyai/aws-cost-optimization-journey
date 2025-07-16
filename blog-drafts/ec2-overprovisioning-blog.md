# How I Saved 70% on EC2 with AWS Compute Optimizer & Spot Instances

## Introduction
When I started reviewing our EC2 usage, I found most instances were over-provisioned.

## Discovery
Using AWS Compute Optimizer, I noticed CPU usage was consistently under 15% on `m5.large` instances.

## Action
- Switched to `t3.medium` for dev/test
- Applied a 1-year no-upfront Savings Plan
- Added Spot Instances with auto-scaling

## Result
- ~70% savings on EC2 spend
- Greater flexibility with similar performance

