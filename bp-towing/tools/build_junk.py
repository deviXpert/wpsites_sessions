import json,copy,random,os,base64,urllib.request,sys
random.seed('junk-car-removal-calgary')
src=json.load(open('ld.json'));ed=copy.deepcopy(json.loads(src['meta']['_elementor_data']))
idx={};par={}
def walk(n,p=None):
    for e in n: idx[e['id']]=e;par[e['id']]=n;walk(e.get('elements',[]),e)
walk(ed)
S=lambda i:idx[i]['settings']
def img(i,mid,url,alt): S(i)['image']={'id':mid,'url':url,'size':'','alt':alt,'source':'library'}
def clone(i,after=True,newsettings=None):
    e=copy.deepcopy(idx[i]);lst=par[i];k=lst.index(idx[i]);lst.insert(k+1 if after else k,e)
    if newsettings: e['settings'].update(newsettings)
    return e
def remove(i): par[i].remove(idx[i])
U='https://bptowingservice.ca/wp-content/uploads/'
P=lambda *xs:''.join(f'<p>{x}</p>' for x in xs)
UL=lambda xs:'<ul>'+''.join(f'<li><strong>{a}:</strong> {b}</li>' for a,b in xs)+'</ul>'
TEL='<a href="tel:+14039912265"><strong>(403) 991-2265</strong></a>'
# HERO
S('402bbaa')['background_slideshow_gallery']=[{'id':4418,'url':U+'2026/08/bp-towing-calgary-1.jpg'},{'id':2867,'url':U+'2026/03/bp-e1772840163330.jpeg'},{'id':2434,'url':U+'2026/02/11-1.webp'}]
S('a2dfaac')['title']='Junk Car Removal Calgary: <span>Cash for Junk Cars</span>'
S('f39acf7')['editor']=P('Have an old, damaged, unwanted, or non-running vehicle taking up space? BP Towing makes junk car removal in Calgary simple and convenient. We buy junk cars, scrap vehicles, and damaged cars in different conditions, whether they still run or no longer start.',
 'If you are looking for cash for junk cars in Calgary, our team can help you arrange vehicle pickup, discuss a competitive offer, and remove your unwanted vehicle without the hassle of trying to drive it to a scrapyard.',
 'We provide towing and junk vehicle pickup throughout Calgary, including NW, NE, SW, SE, and other parts of the city. Our goal is to make the process straightforward, from your first call to the removal of your vehicle.')
S('bc2f5f5')['editor']=f'<p>📞 Call BP Towing at {TEL} to discuss your junk car and arrange pickup.</p>'
S('0b86c82')['text']='Call Now: (403) 991-2265'
clone('0b86c82',after=False,newsettings={'text':'Get in Touch','link':{'url':'https://bptowingservice.ca/contact/','is_external':'','nofollow':'','custom_attributes':''},'selected_icon':{'value':'fas fa-paper-plane','library':'fa-solid'},'_css_classes':'bp-btn bp-btn-white'})
# SPLIT 1
S('d58ede8')['title']='Cash for Junk Cars <span>Calgary</span>'
S('87ade91')['editor']=P('Selling an old or damaged vehicle privately can take time, especially when it needs expensive repairs or cannot be driven. You may have to create listings, respond to buyers, arrange inspections, and find a way to transport the vehicle.',
 'BP Towing offers a more convenient option for people looking to sell or remove unwanted vehicles in Calgary. We consider junk cars, scrap vehicles, and damaged cars, helping owners explore a practical solution without arranging separate transportation themselves.',
 "When you contact us, share your vehicle's year, make, model, condition, and pickup location. Our team can discuss your vehicle and provide information about the available options.")
img('7b68794',2281,U+'2026/02/photo_2026-02-14_11-20-37.webp','BP Towing flatbed ready for junk car removal in Calgary')
# DARK GRID: why contact
S('3775161')['title']='Why Contact BP Towing for <span>Junk Car Removal?</span>'
cards=[('e3da429','fas fa-truck-pickup','Convenient vehicle pickup','Arrange towing instead of trying to drive a vehicle that no longer runs.'),
('6ebfb42','fas fa-dollar-sign','Cash offers for eligible vehicles','Ask about an offer for your junk, scrap, or damaged car.'),
('722caa7','fas fa-truck-moving','Free towing','Vehicle removal includes free towing under the service terms confirmed with our team.'),
('043e84d','fas fa-car-crash','Different vehicle conditions','Contact us about old, damaged, scrap, or non-running vehicles.'),
('913aba5','fas fa-map-marked-alt','Calgary-wide coverage',"We provide towing throughout Calgary's NW, NE, SW, SE, and other city areas."),
('f68c7b2','fas fa-handshake','Straightforward arrangements','Discuss your vehicle, offer, pickup location, and scheduling directly with our team.')]
for i,ic,t,dsc in cards: S(i).update({'selected_icon':{'value':ic,'library':'fa-solid'},'title_text':t,'description_text':dsc})
remove('25308a5');remove('613d961')
S('e433ce5')['css_classes']=S('e433ce5')['css_classes'].replace('bp-grid-4','bp-grid-3')
note=clone('3775161',newsettings={})  # placeholder replaced below
par['3775161'].remove(note)
n=copy.deepcopy(idx['6eff33a']);n['settings']['editor']='<p>Our team can explain the next steps and confirm the details before arranging your vehicle pickup.</p>';n['settings']['_css_classes']='bp-lead bp-note-c'
idx['44e05a8']['elements'].append(n)
# AREAS
S('14a5163')['title']='Junk Car Removal <span>Across Calgary</span>'
S('6eff33a')['editor']=P('BP Towing provides towing services throughout Calgary, making it convenient to discuss junk car pickup wherever your vehicle is located within the city. We cover:')
areas=[('949ed97','56168b8','North West Calgary (NW)','Junk vehicle pickup enquiries throughout NW Calgary.'),
('ff188d0','e06c28f','North East Calgary (NE)','Contact us to arrange pickup in NE Calgary.'),
('3a12330','dcf66ea','South East Calgary (SE)','Discuss removal options for vehicles in SE Calgary.'),
('a5ca798','0534525','South West Calgary (SW)','Arrange towing for eligible junk vehicles in SW Calgary.'),
('629d541','22f4c2f','North and South Calgary','Contact our team with your exact pickup location.'),
('c252fb1','1ecb974','East and West Calgary','We can discuss your vehicle pickup requirements.'),
('aeb92be','d259baa','Downtown Calgary','Ask about towing access and pickup arrangements in central Calgary.')]
for h,t,a,b in areas: S(h)['title']=a;S(t)['editor']=P(b)
S('54e1102')['editor']=P('We also accept enquiries for vehicle pickup outside Calgary, including nearby Alberta communities. Availability, timing, and any applicable conditions must be confirmed with our team.',
 'If you are searching for <strong>junk car removal near me</strong> or <strong>cash for junk cars Calgary</strong>, contact BP Towing with your location and vehicle details to find out how we can help.')
# TYPES split
S('d67e5d0')['title']='What Types of <span>Junk Cars</span> Do We Remove?'
S('022c05b')['_css_classes']='bp-t bp-list'
S('022c05b')['editor']=P('Not every unwanted vehicle is completely worthless, and not every damaged car needs the same removal solution. BP Towing can discuss different vehicle conditions and help determine whether we can assist with your pickup.')+UL([
('Scrap Cars','If your vehicle has reached the end of its useful life, scrap car removal can be a practical way to clear space in your driveway, garage, or parking area. Contact us with your vehicle details to discuss removal options.'),
('Non-Running Cars','A car that will not start can be difficult to sell or transport. Whether the issue involves the battery, engine, transmission, or another mechanical problem, tell us about its condition when requesting junk car pickup in Calgary.'),
('Accident-Damaged Vehicles','Accidents can leave vehicles with body damage, mechanical problems, or costly repair requirements. If your vehicle has been damaged in a collision and you no longer want to keep it, contact BP Towing to discuss removal and any available offer.'),
('Old and Unwanted Cars','An older vehicle may no longer be reliable or worth repairing. If your unused car is taking up valuable space, we can discuss a suitable pickup arrangement.'),
('Cars With Major Mechanical Problems','Engine failure, transmission trouble, extensive rust, and other serious mechanical issues can make repairs uneconomical. Explain the problem and the overall condition of your vehicle so our team can assess the available options.'),
('Trucks, SUVs, and Other Vehicles','If you have an unwanted truck, SUV, or another vehicle, contact us with its year, make, model, condition, and location. We can confirm whether the vehicle is suitable for our junk car service.')])
img('5df96e0',2434,U+'2026/02/11-1.webp','Damaged pickup truck loaded on a BP Towing flatbed for removal')
# ONECALL: why choose
S('b48da23')['title']='Why Choose BP Towing for <span>Junk Car Removal?</span>'
intro=copy.deepcopy(idx['87ade91']);intro['settings']['editor']=P('Choosing a vehicle removal service should be about more than finding a tow truck. You also need clear communication about the vehicle, the offer, and the pickup arrangements.',
 'BP Towing brings its towing experience to junk vehicle pickup across Calgary. Our existing towing services help customers arrange vehicle transportation when a car is no longer suitable to drive. When contacting us, you can discuss:')
intro['settings']['_css_classes']='bp-t'
oc=idx['327705b']['elements'];oc.insert(1,intro)
rows=[('7bc3e7c','fas fa-car','Your vehicle','The condition and location of your vehicle.'),
('400be22','fas fa-recycle','Removal options','Available junk car removal options.'),
('9ce85c1','fas fa-dollar-sign','Cash offer','Whether a cash offer is available for your vehicle.'),
('86269a8','fas fa-truck-pickup','Towing & access','Towing arrangements and pickup access.'),
('303df93','fas fa-file-invoice-dollar','Fees & conditions','Any applicable removal fees or conditions.'),
('d8699bd','fas fa-file-signature','Documents & payment','The documents and payment details needed before collection.')]
for i,ic,t,dsc in rows: S(i).update({'selected_icon':{'value':ic,'library':'fa-solid'},'title_text':t,'description_text':dsc})
remove('b05e5d5');remove('36dd9aa')
outro=copy.deepcopy(intro);outro['settings']['editor']=P('We aim to make the process clear so you can make an informed decision about your unwanted vehicle.');oc.append(outro)
img('6c11660',2867,U+'2026/03/bp-e1772840163330.jpeg','BP Towing flatbed carrying a vehicle in Calgary')
# TIMELINE
S('812f00c')['title']='How Junk Car Removal <span>Works in Calgary</span>'
tl=copy.deepcopy(idx['6eff33a']);tl['settings']['editor']=P('Arranging junk car removal does not need to be complicated. Here is how to get started with BP Towing.');idx['23f9100']['elements'].append(tl)
steps=[('a48ad94','fdb66f2','Step 1: Contact Our Team',P(f'Call {TEL} and tell us that you need junk car removal in Calgary. Provide the vehicle\'s year, make, model, general condition, and current location.')),
('2f2cbda','7248e8a','Step 2: Discuss Your Vehicle and Offer',P("Our team will discuss the vehicle information and available options with you. If you are looking for cash for junk cars, ask about an offer based on the vehicle's condition and details.",'Before proceeding, confirm the agreed amount, any applicable conditions, and the pickup arrangements.')),
('81756db','079c72f','Step 3: Arrange Vehicle Pickup',P('Once the details are confirmed, coordinate a suitable pickup time with our team. Let us know if the vehicle is in a driveway, parking lot, underground parkade, or another location that could affect towing access.')),
('654e133','b06ffae','Step 4: Confirm the Details and Complete Removal',P('Before the vehicle is collected, confirm any required ownership documents, the agreed payment arrangements, and the towing details. Our team will explain the next steps so you know what to expect.'))]
for h,t,a,b in steps: S(h)['title']=a;S(t)['editor']=b
remove('8f5b97c')
end=copy.deepcopy(idx['6eff33a']);end['settings']['editor']=f'<p>Ready to discuss your unwanted vehicle? Call BP Towing at {TEL}.</p>';end['settings']['_css_classes']='bp-lead bp-note-c'
idx['f680e54']['elements'].append(end)
# WORTH
S('7f6613f')['title']='How Much Is a Junk Car <span>Worth in Calgary?</span>'
S('28707fb')['editor']=P('The value of a junk car depends on more than its age. Two vehicles of the same make and model may have different values because of their condition, parts, and current scrap market conditions.','Factors that may influence an offer include:')+UL([
('Year, make, and model','Vehicle demand and the availability of reusable parts can affect its potential value.'),
('Overall condition','Rust, accident damage, missing components, and mechanical problems may influence an offer.'),
('Running condition','Whether the vehicle starts and can be driven is useful information when assessing it.'),
('Parts and scrap value',"Reusable components and recoverable metal may contribute to the vehicle's value."),
('Vehicle completeness','Missing engines, wheels, batteries, or other parts can affect the assessment.')])+P('There is no single price that applies to every junk car in Calgary. For a more relevant assessment, provide accurate vehicle details and ask BP Towing about an offer.','We recommend confirming the agreed price and any towing conditions before scheduling collection.')
img('b66b1e9',4418,U+'2026/08/bp-towing-calgary-1.jpg','Flatbed tow truck collecting an unwanted pickup truck in Calgary')
# remove tips
remove('ecd4ef4')
# FAQ
faq=[('Where can I get junk car removal in Calgary?',f"BP Towing provides towing throughout Calgary, including NW, NE, SW, SE, and other city areas. Contact us at {TEL} with your vehicle's location to discuss junk car pickup."),
('Does BP Towing offer cash for junk cars in Calgary?','Yes. BP Towing offers cash for junk cars, scrap vehicles, and damaged cars. Contact our team with your vehicle details to discuss an offer and confirm the applicable conditions.'),
('Can I sell a car that does not run?','You can contact BP Towing about non-running vehicles. Tell us whether the car has engine trouble, transmission problems, a dead battery, or another issue so we can discuss suitable pickup options.'),
('Does junk car removal include free towing?','Yes. BP Towing offers free towing with its junk car removal service. Confirm the pickup location, eligibility, and any applicable conditions with our team before arranging collection.'),
('How much can I get for my junk car in Calgary?',"The amount depends on factors such as the vehicle's year, make, model, condition, completeness, and potential scrap or parts value. Contact BP Towing for an assessment of your specific vehicle."),
('Do you remove accident-damaged cars?','Yes. BP Towing offers removal options for damaged vehicles. Share details about the accident damage and whether the vehicle can roll or steer so the team can discuss the appropriate towing arrangements.'),
('Do I need to repair my car before junk car removal?','You do not necessarily need to repair a vehicle before asking about removal. Contact BP Towing and explain the condition of your car to confirm whether it can be collected as it is.'),
('What information should I provide when requesting junk car pickup?',"Provide the vehicle's year, make, model, condition, pickup address or area, and whether it is accessible to a tow truck. You should also ask which ownership documents are required."),
('Can you pick up a junk car from a driveway or parking lot?','Tell us where the vehicle is parked and whether there are any access restrictions. Underground parkades, tight spaces, and vehicles with locked wheels may require additional arrangements.'),
('Does BP Towing provide junk car pickup outside Calgary?','Pickup outside Calgary may be available upon request. Contact our team with your Alberta community and vehicle details to confirm availability, pricing, and scheduling.'),
('How do I arrange junk car removal with BP Towing?',f"Call {TEL}, explain your vehicle's condition, and provide its location. Discuss the available offer, towing arrangements, and any requirements before confirming the pickup.")]
S('054b17b')['title']='Frequently Asked Questions About <span>Junk Car Removal in Calgary</span>'
acc=idx['674168c'];acc['settings']['items']=acc['settings']['items'][:len(faq)];acc['elements']=acc['elements'][:len(faq)]
for k,(q,a) in enumerate(faq):
    acc['settings']['items'][k]['item_title']=q;acc['elements'][k]['elements'][0]['settings']['editor']=P(a)
# CTA
S('539bda7')['title']='Get Started With Junk Car Removal Calgary'
S('8503b47')['editor']=P('If you have an old, damaged, scrap, or non-running vehicle taking up space, BP Towing can help you explore your junk car removal options.',
 "Contact us to discuss your vehicle, arrange towing, and find out whether a cash offer is available. We serve Calgary's NW, NE, SW, SE, and other city areas, with additional pickup enquiries considered outside Calgary.",
 f'📞 Call BP Towing today at {TEL} to discuss cash for junk cars in Calgary.')
items=['Junk car removal','Cash for junk cars','Scrap car pickup','Non-running vehicles','Accident-damaged cars','Free towing','Calgary-wide pickup','Trucks & SUVs']
sp=''.join(f'<span>{x}</span>' for x in items)+''.join(f'<span aria-hidden="true">{x}</span>' for x in items)
S('f034226')['html']=f'<div class="bp-tk"><div class="bp-tk-track">{sp}</div></div>'
# new ids
def reid(n):
    for e in n: e['id']='%07x'%random.getrandbits(28);reid(e.get('elements',[]))
reid(ed)
blob=json.dumps(ed)
import re
for m in re.finditer("ong distance|\\u2013|\\u2014",blob,re.I): print(blob[max(0,m.start()-150):m.end()+60])
json.dump(ed,open('junk_ed.json','w'))
print('ok',len(blob))
