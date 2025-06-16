#!/usr/bin/env python3
import os

# Root folder to scan
ROOT_DIR = "extracted"

# ─── Paste your exact navbar block here ───
NAVBAR = """
About

Services

## BSGI

BSGI

#### Business Services & Growth Incubation

Business Services & Growth Incubation

## FTPS

FTPS

#### Financial Technology & Payment Solutions

Financial Technology & Payment Solutions

<img src="https://www.occamsadvisory.com/wp-content/uploads/menu/1_1.svg" alt="">

## CMIB

CMIB

#### Capital Markets & Investment Banking

Capital Markets & Investment Banking

<img src="https://www.occamsadvisory.com/wp-content/uploads/menu/1_1.svg" alt="">

## TC

TC

#### Tax Credits

Tax Credits

Structure, Incorporation &

Accounting
                                                        Advisory

Beneficial Ownership Information
                                                        Report

Process Efficiency, Compliance,

Tax
                                                        Planning & Filing

Brand Building, Mobile Marketing &

Data
                                                        Analytics

Digital
                                                        Presence & Social Media

Information
                                                        Technology Services

Merchant
                                                        Accounts Across the Globe

Tailored Payment Solutions &

Verification
                                                        Service

Customized Payment Risk

Management &
                                                        Analytics

Proprietary
                                                        Fintech Platform

Capital
                                                        Raising to Promote Growth

Financial Advisory &

Transaction
                                                        Integration

Sell-Side M&A

Buy-Side M&A

Decision
                                                        Science and Risk Assurance

Employee
                                                        Retention Credit (ERC)

Audit Advisory

News

FAQs

Research & Development (R&D)

Self-Employed Tax
                                                        Credit (SETC)

Team

Resources

## BLOGS >

BLOGS >

Insights and expert opinions on business growth, innovation, and
                                                    trends. Stay updated with our latest articles and thought leadership
                                                    pieces.

## PODCAST & WEBINAR >

PODCAST & WEBINAR >

Engage with industry experts through our podcasts and webinars.
                                                    Discover valuable insights and strategies for business success.

## EVENTS >

EVENTS >

Join our events to connect with professionals, gain knowledge, and
                                                    explore new opportunities. Stay informed about upcoming conferences
                                                    and seminars.

## MICRO INSIGHTS >

MICRO INSIGHTS >

Quick, actionable insights on various business topics. Enhance your
                                                    knowledge with our concise and informative micro insights.

## RECOGNITIONS >

RECOGNITIONS >

Explore the awards and recognitions that highlight our commitment to
                                                    excellence and innovation. See how we stand out in the industry.

## MEDIA MENTIONS >

MEDIA MENTIONS >

Read about Occams Advisory in the news. Discover how we are making an
                                                    impact and gaining recognition from media outlets.

## TESTIMONIALS >

TESTIMONIALS >

Hear from our satisfied clients. Watch video testimonials that
                                                    showcase our successful projects and client experiences.

## PRESS RELEASE >

PRESS RELEASE >

Stay updated with our latest announcements and developments. Read our
                                                    press releases for news about our achievements and initiatives.

Contact

Login
"""  

TOP3AWARDS ="""
# Top 3 Awards
                    in
                    2025

Top 3 Awards
                    in
                    2025

Celebrating Excellence: Top Accolades in Business and Workplace Environment

# FORTUNE AMERICA’S

FORTUNE AMERICA’S

###### Most Innovative CompaniesAward list – 2023.

Most Innovative Companies

Award list – 2023.

This award recognizes Occams Advisory for its excellence in product
                        innovation,
                        process
                        innovation, and innovation culture, as selected by Fortune and Statista Inc..

# Financial Times’ The Americas’ Fastest-Growing Companies - 2020
                            to
                            2023, 2025

Financial Times’ The Americas’ Fastest-Growing Companies - 2020
                            to
                            2023, 2025

###### Rank 159

Rank 159

Occams Advisory is thrilled to be recognized in the Financial Times' 2025
                            list of the Americas' Fastest-Growing Companies. This achievement underscores our relentless
                            pursuit of excellence and innovation, driving sustained growth and industry leadership.

# INC 5000

INC 5000

###### Fastest Growing US Companies – 2016 to 2021, 2023 and 2024

Fastest Growing US Companies – 2016 to 2021, 2023 and 2024

This marks the eight time in nine years that the company has been
                            recognized
                            on this
                            prestigious
                            list of the fastest-growing private companies in America.

# INC 5000

INC 5000

###### Fastest Growing US Companies – 2016 to 2021, 2023 and 2024

Fastest Growing US Companies – 2016 to 2021, 2023 and 2024

This marks the eight time in nine years that the company has been
                            recognized
                            on this
                            prestigious
                            list of the fastest-growing private companies in America.

# FORTUNE AMERICA’S

FORTUNE AMERICA’S

###### Most Innovative CompaniesAward list – 2023.

Most Innovative Companies

Award list – 2023.

This award recognizes Occams Advisory for its excellence in product
                        innovation,
                        process
                        innovation, and innovation culture, as selected by Fortune and Statista Inc..

# Financial Times’ The Americas’ Fastest-Growing Companies -
                                2020
                                to
                                2023, 2025

Financial Times’ The Americas’ Fastest-Growing Companies -
                                2020
                                to
                                2023, 2025

###### Rank 159

Rank 159

Occams Advisory is thrilled to be recognized in the Financial Times'
                                2025
                                list of the Americas' Fastest-Growing Companies. This achievement underscores our
                                relentless
                                pursuit of excellence and innovation, driving sustained growth and industry leadership.

# INC 5000

INC 5000

###### Fastest Growing US Companies – 2016 to 2021, 2023 and 2024

Fastest Growing US Companies – 2016 to 2021, 2023 and 2024

This marks the eight time in nine years that the company has been
                            recognized
                            on this
                            prestigious
                            list of the fastest-growing private companies in America.

# FORTUNE AMERICA’S

FORTUNE AMERICA’S

###### Most Innovative CompaniesAward list – 2023.

Most Innovative Companies

Award list – 2023.

This award recognizes Occams Advisory for its excellence in product
                        innovation,
                        process
                        innovation, and innovation culture, as selected by Fortune and Statista Inc..

1

2

3

View All
                    Awards
"""





Unleash_THEOCCAMS_WAY = """
# Unleash THEOCCAMS WAY

Unleash THE

OCCAMS WAY

We offer a FREE 30-minute consultation to help you identify
                    areas of your business or personal finances where you can get
                    immediate results by using our evidence-based approach to superior results.

Grow your Company with us

# Get Instant Help

Get Instant Help

Get in touch with our team via live chat. They are available 24x7.

# Buzz us in! We will reply within 2-4 business hours.

Buzz us in! We will reply within 2-4 business hours.

Call

Chat Support

Book
                            a Free

Consultation

Email

# Unleash THEOCCAMS WAY

Unleash THE

OCCAMS WAY

We offer a FREE 30-minute consultation to help you identify
                    areas of your business or personal finances where you can get
                    immediate results by using our evidence-based approach to superior results.

Grow your Company with us

# Get Instant Help

Get Instant Help

Get in touch with our team via live chat. They are available 24x7.

# Buzz us in! We will reply within 2-4 business hours.

Buzz us in! We will reply within 2-4 business hours.

Call

Chat Support

Book
                            a Free  Consultation

Email
"""

Interactive_Product_Tour = """
# Interactive Product Tour

Interactive Product Tour

Get a hands-on feel for our platform before you sign up. Our interactive tour
                            guides you through
                            the key features of boireporting.io, showing you how easy it is to manage your compliance needs
                            with our software.

##### US-Based

US-Based

Occams Advisory is proudly headquartered and operated in the
                                United
                                States.
                                Unlike foreign- based competitors, we are regulated by stringent US laws, ensuring the
                                highest standards of security and compliance.

##### Secure API

Secure API

We use API technology to transmit Beneficial Ownership
                                Information Reports
                                (BOIR) in real-time. While other services may manually file your information, posing
                                security risks and potential errors, our process ensures instant and secure filings.

</p

##### Trusted

Trusted

Occams Advisory was founded by US-based professionals with
                                decades of
                                technology and industry experience. We collaborate with US organizations to educate, inform,
                                and facilitate compliance with the CTA. These firms have trust in our expertise and
                                commitment to protecting your data.
"""

#=========================================

Clients_Testimonials = """
# Clients
                            Testimonials

Clients
                            Testimonials

Real
                        Feedback
                        from Our Clients: Hear What They Have to Say

TrustBox widget - Mini Carousel

TrustBox widget - Mini

End TrustBox widget

End TrustBox widget

# Great experience
                                All of the people I worked with were very professional and prompt in answering all the
                                questions I had.
                                Great Job!! To all involved

Great experience
                                All of the people I worked with were very professional and prompt in answering all the
                                questions I had.
                                Great Job!! To all involved

###### Bill Wegleitner

Bill Wegleitner

# Working with Occams was a fantastic experience. They were excellent
                                communicators and came
                                through on all of their promises. I was a little skeptical of at first, as I am sure most
                                people
                                were, but they delivered!

Working with Occams was a fantastic experience. They were excellent
                                communicators and came
                                through on all of their promises. I was a little skeptical of at first, as I am sure most
                                people
                                were, but they delivered!

###### Rye Nazarian

Rye Nazarian

# All representatives were very knowledgeable and customer service
                                oriented. I felt they
                                wanted to
                                assist me and insure my needs were met. All my questions and concerns were addressed in a
                                caring
                                and professional manner- Thank you Fidelity and OCCAMS for your support in this effort!!!!!

All representatives were very knowledgeable and customer service
                                oriented. I felt they
                                wanted to
                                assist me and insure my needs were met. All my questions and concerns were addressed in a
                                caring
                                and professional manner- Thank you Fidelity and OCCAMS for your support in this effort!!!!!

###### Bennie O Brooks

Bennie O Brooks

# The company was clear in what they needed from us to get the
                                application submitted, and they
                                handled the rest. They do not get paid until you do.

The company was clear in what they needed from us to get the
                                application submitted, and they
                                handled the rest. They do not get paid until you do.

###### Susan Szymborski

Susan Szymborski

# Did exactly what they said they would do and they got us all this money
                                that we didn’t even
                                know
                                about. Very easy and pleasant experience.

Did exactly what they said they would do and they got us all this money
                                that we didn’t even
                                know
                                about. Very easy and pleasant experience.

###### Jeremy Henri

Jeremy Henri

# Great experience
                                All of the people I worked with were very professional and prompt in answering all the
                                questions I had.
                                Great Job!! To all involved

Great experience
                                All of the people I worked with were very professional and prompt in answering all the
                                questions I had.
                                Great Job!! To all involved

###### Bill Wegleitner

Bill Wegleitner

# Working with Occams was a fantastic experience. They were excellent
                                communicators and came
                                through on all of their promises. I was a little skeptical of at first, as I am sure most
                                people
                                were, but they delivered!

Working with Occams was a fantastic experience. They were excellent
                                communicators and came
                                through on all of their promises. I was a little skeptical of at first, as I am sure most
                                people
                                were, but they delivered!

###### Rye Nazarian

Rye Nazarian

1

2

3

4

5
"""

#==========================================

blog_insights = """
# Blogs: Insights
                    &
                    Thought
                    Leadership

Blogs: Insights
                    &
                    Thought
                    Leadership

Explore Our Latest
                Articles on Business Growth and Innovation

##### Beyond Aesthetics: How Strategic Graphic Design Drives Business Growth

Beyond Aesthetics: How Strategic Graphic Design Drives Business Growth

May 27, 2025

Blog At A Glance: Introduction The Role of Graphic Designer   The Indispensable Value of Graphic Design  The Importance of Graphic Design Trends  Key Graphic Design Trends for 2025 Conclusion   IntroductionAs a seasoned graphic designer, I've witnessed firsthand...

Read More

##### THE POWER BEHIND THE SCENES

THE POWER BEHIND THE SCENES

May 20, 2025

Blog At A Glance: Introduction Role of Backend Customer Support in Financial Organizations  Beyond the Frontlines: What Backend Support Really Does  Why Backend Teams are Critical to Client Trust  Growth and Competitive Edge Through Strong Backend Operations  Key...

Read More

##### In 2025, Brands That Embrace Art Will Lead the Future

In 2025, Brands That Embrace Art Will Lead the Future

May 12, 2025

Blog At A Glance: Introduction A Return to Art as the Core of Branding  Building Brands as Worlds, Not Just Products  Beyond Audiences: Brands Must Build Communities  From Transactions to Cultural Movements Introduction When you close your eyes and picture a tube of...

Read More

##### In 2025, Brands That Embrace Art Will Lead the Future

In 2025, Brands That Embrace Art Will Lead the Future

May 12, 2025

Blog At A Glance: Introduction A Return to Art as the Core of Branding  Building Brands as Worlds, Not Just Products  Beyond Audiences: Brands Must Build Communities  From Transactions to Cultural Movements Introduction When you close your eyes and picture a tube of...

Read
                                    More

##### Beyond Aesthetics: How Strategic Graphic Design Drives Business Growth

Beyond Aesthetics: How Strategic Graphic Design Drives Business Growth

May 27, 2025

Blog At A Glance: Introduction The Role of Graphic Designer   The Indispensable Value of Graphic Design  The Importance of Graphic Design Trends  Key Graphic Design Trends for 2025 Conclusion   IntroductionAs a seasoned graphic designer, I've witnessed firsthand...

Read More

##### THE POWER BEHIND THE SCENES

THE POWER BEHIND THE SCENES

May 20, 2025

Blog At A Glance: Introduction Role of Backend Customer Support in Financial Organizations  Beyond the Frontlines: What Backend Support Really Does  Why Backend Teams are Critical to Client Trust  Growth and Competitive Edge Through Strong Backend Operations  Key...

Read More

##### In 2025, Brands That Embrace Art Will Lead the Future

In 2025, Brands That Embrace Art Will Lead the Future

May 12, 2025

Blog At A Glance: Introduction A Return to Art as the Core of Branding  Building Brands as Worlds, Not Just Products  Beyond Audiences: Brands Must Build Communities  From Transactions to Cultural Movements Introduction When you close your eyes and picture a tube of...

Read
                                    More

##### Beyond Aesthetics: How Strategic Graphic Design Drives Business Growth

Beyond Aesthetics: How Strategic Graphic Design Drives Business Growth

May 27, 2025

Blog At A Glance: Introduction The Role of Graphic Designer   The Indispensable Value of Graphic Design  The Importance of Graphic Design Trends  Key Graphic Design Trends for 2025 Conclusion   IntroductionAs a seasoned graphic designer, I've witnessed firsthand...

Read More

1

2

3

Browse All
"""

#===========================================

Leadership_Team = """
# Leadership TeamLeading BSGI with strategic vision, tax expertise, and efficiency to
                                empower client growth.

Leadership Team

Leading BSGI with strategic vision, tax expertise, and efficiency to
                                empower client growth.

#### David King

David King

Deputy CEO

Read More

#### Vardhman Shah

Vardhman Shah

COO (Chief Operating Officer)

Read More

#### Amber E Kellogg

Amber E Kellogg

VP - Affiliate Origination & Management

Read More

Browse More Members
"""

# List your patterns (variables) here:
PATTERNS = [
    NAVBAR,
    TOP3AWARDS,
    Unleash_THEOCCAMS_WAY,
    Clients_Testimonials,
    Interactive_Product_Tour,
    blog_insights,
    Leadership_Team,

    # another_block,
]

# ─── END CONFIG ────────────────────────────────────────────────────────────────

def find_md_files(root):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith('.md'):
                yield os.path.join(dirpath, fn)

def dedupe_pattern(pattern):
    seen = False
    for path in sorted(find_md_files(ROOT_DIR)):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if pattern not in content:
            continue

        if not seen:
            # keep first occurrence, strip extras in this file
            idx = content.find(pattern) + len(pattern)
            first_chunk = content[:idx]
            remainder   = content[idx:].replace(pattern, "")
            new_content = first_chunk + remainder
            seen = True
        else:
            # remove all occurrences
            new_content = content.replace(pattern, "")

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[UPDATED] {path}")

def main():
    if not os.path.isdir(ROOT_DIR):
        print(f"Error: folder '{ROOT_DIR}' not found in current directory.")
        return
    for block in PATTERNS:
        dedupe_pattern(block)

if __name__ == "__main__":
    main()