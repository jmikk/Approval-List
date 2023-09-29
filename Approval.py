import requests
import xml.etree.ElementTree as ET


def get_approvals_for_proposal(proposal_id, xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the proposal element with the given ID
    proposal_element = None
    for proposal in root.findall(".//PROPOSAL"):
        if proposal.get("id") == proposal_id:
            proposal_element = proposal
            break

    # If the proposal element was found
    if proposal_element:
        # Get the list of approvals
        approvals = proposal_element.find("APPROVALS")

        if approvals is not None:
            approval_list = approvals.text.split(":")
            return approval_list
        else:
            return []
    else:
        return []


# Ask the user for the User-Agent header
user_agent = input("Enter User-Agent header: ")

# Set the headers with the provided User-Agent
headers = {"User-Agent": user_agent}

# Send a request to the first API to get the type of council (SC or GA)
url = "https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=delegates"
response = requests.get(url, headers=headers)

root = ET.fromstring(response.text)
delegates = root.find("DELEGATES").text
delegates = delegates.split(",")


if response.status_code == 200:
    council_type = input("What council? 1 for SC or 2 for GA")
    # Parse the response to get the council type (1 for SC, 2 for GA)

    proposals_url = (
        f"https://www.nationstates.net/cgi-bin/api.cgi?wa={council_type}&q=proposals"
    )

    # Send a request to the proposals API
    proposals_response = requests.get(proposals_url, headers=headers)

    proposal_id = input("Enter the ID of your proposal: ")
    approvals = get_approvals_for_proposal(proposal_id, proposals_response.text)
    delegates_without_approvals = [
        delegate for delegate in delegates if delegate not in approvals
    ]
    output_file = "output.txt"

    # Open the output file in write mode
    with open(output_file, "w") as file:
        for i, delegate in enumerate(delegates_without_approvals):
            if i % 8 == 0 and i != 0:
                # Start a new line after every 8 names
                file.write("\n")
            if i != 0:
                # Add a comma and a space after each name except the first one
                file.write(", ")
            file.write(delegate)
    print("All done and good luck with your proposal")

else:
    print(f"Error fetching council type data. Status code: {response.status_code}")
