from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Sample data
reviews = ["\"The Student of Prague\" is an early feature-length horror drama or, rather, it is an \"autorenfilm\" (i.e. an author's film). It's a piece of a movement of many movements that tried to lend cultural respectability to cinema, or just make a profit, by adapting literature or theatre onto the screen. Fortunately, the story of this book with moving pictures is good. Using Alfred de Musset's poem and a story by Edgar Allen Poe, it centers on a doppelg\u00e4nger theme.Unfortunately, the most cinematic this film gets is the double exposure effects to make Paul Wegener appear twice within scenes. Guido Seeber was a special effects wizard for his day, but he's not very good at positioning the camera or moving it. Film scholar Leon Hunt (printed in \"Early Cinema: Space, Frame, Narrative\"), however, has made an interesting analysis on this film using framing to amplify the doubles theme: characters being split by left/right, near/far and frontal/diagonal framing of characters and shots. Regardless, the film mostly consists of extended long shots from a fixed position, which is noticeably primitive. Worse is the lack of editing; there's very little scene dissection and scenes linger. None of this is unusual for 1913, but there were more advanced pictures in this respect around the same time, including the better parts of \"Atlantis\" (August Blom, 1913), \"Twilight of a Woman's Soul\" (Yevgeni Bauer, 1913) and the short films of D.W. Griffith.An expanded universal film vocabulary by 1926 would allow for a superior remake. Furthermore, the remake has a reason for the Lyduschka character--other than being an occasional troublemaker and spectator surrogate. Here, the obtrusively acted gypsy lurks around, seemingly, with a cloak of invisibility. I know their world is silent to me, but I assume, with their lips moving and such, that their world would not be silent to them, so how can Lyduschka leer over others' shoulders and not be noticed?Nevertheless, this is one of the most interesting early films conceptually. Wegener, who seems to have been the primary mind behind it, in addition to playing the lead, would later play the title role and co-direct \"The Golem\" in 1920--helping to further inaugurate a dark, supernatural thread in German silent cinema.(Note: The first version I viewed was about an hour long (surely not quite complete) and was in poor condition, with faces bleached at times and such. I'm not sure who was the distributor. I've also since seen the Alpha DVD, which, at 41 minutes, is missing footage present in the aforementioned print and also has fewer and very different title cards, but is visually not as bad. The repetitive score is best muted, though.)", "It was okay.", "Horrible film!", "Decent, but could be better.", "Amazing cinema experience!", "Average movie.", "A solid 7/10 film.", "Waste of time.", "I'd rate it 6/10.", "One of the best movies ever."]
ratings = [7, 5, 1, 6, 10, 5, 7, 2, 6, 10]  # Ratings from 1 to 10

# Split data
X_train, X_test, y_train, y_test = train_test_split(reviews, ratings, test_size=0.2, random_state=42)

# Convert text data into TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Logistic Regression model
clf = LogisticRegression(max_iter=1000)  # Increase max_iter for better convergence with more classes
clf.fit(X_train_vec, y_train)

# Predict on test set
y_pred = clf.predict(X_test_vec)

# Evaluate the model
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
