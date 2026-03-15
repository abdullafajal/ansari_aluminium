from dynamic_preferences.types import StringPreference, LongStringPreference, FilePreference, BooleanPreference
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.preferences import Section

# We compile the registry using the global_preferences_registry

contact = Section('contact')
stats = Section('stats')

# Section: Contact Info
@global_preferences_registry.register
class SiteAddress(LongStringPreference):
    section = contact
    name = "address"
    default = "D-01, Sector Chi V, Opposite Amarpali Society, Greater Noida, UP 201312"
    verbose_name = "Office Address"

@global_preferences_registry.register
class SiteMapLink(StringPreference):
    section = contact
    name = "map_link"
    default = "https://www.google.com/maps/dir//UPVC+Club,+D-01,+Sector,+opposite+Amarpali+society,+Chi+V,+Chuharpur+Khadar,+Greater+Noida,+Uttar+Pradesh+201312/@28.6861914,77.2749958,14z/data=!4m8!4m7!1m0!1m5!1m1!1s0x390cc10069132473:0x417f0376636d449!2m2!1d77.5086991!2d28.4284287?entry=ttu&g_ep=EgoyMDI2MDIwNC4wIKXMDSoASAFQAw%3D%3D"
    verbose_name = "Google Maps Link"

@global_preferences_registry.register
class SitePhone(StringPreference):
    section = contact
    name = "phone"
    default = "+919582010747"
    verbose_name = "Phone Number"

@global_preferences_registry.register
class SiteEmail(StringPreference):
    section = contact
    name = "email"
    default = "abdullafajal@gmail.com"
    verbose_name = "Email Address"

@global_preferences_registry.register
class ShowWhatsAppButton(BooleanPreference):
    section = contact
    name = "show_whatsapp_button"
    default = True
    verbose_name = "Show Floating WhatsApp Button"

# Section: Key Stats
@global_preferences_registry.register
class SiteXP(StringPreference):
    section = stats
    name = "experience"
    default = "3+"
    verbose_name = "Years of Experience"

@global_preferences_registry.register
class SiteProjects(StringPreference):
    section = stats
    name = "projects"
    default = "50+"
    verbose_name = "Projects Completed"

@global_preferences_registry.register
class SiteWarranty(StringPreference):
    section = stats
    name = "warranty"
    default = "15yr"
    verbose_name = "Profile Warranty"

@global_preferences_registry.register
class SiteDelivery(StringPreference):
    section = stats
    name = "delivery"
    default = "100%"
    verbose_name = "On-Time Delivery"

@global_preferences_registry.register
class SiteGoogleRating(StringPreference):
    section = stats
    name = "google_rating"
    default = "5.0"
    verbose_name = "Google Rating"

# Section: About Page
about = Section('about')

@global_preferences_registry.register
class AboutHeroImage(StringPreference):
    section = about
    name = "hero_image"
    default = "https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=2070&auto=format&fit=crop"
    verbose_name = "Hero Image (URL)"

@global_preferences_registry.register
class AboutHeroImageFile(FilePreference):
    section = about
    name = "hero_image_file"
    default = None
    verbose_name = "Hero Image (Upload)"

@global_preferences_registry.register
class AboutApproachImage(StringPreference):
    section = about
    name = "approach_image"
    default = "https://images.unsplash.com/photo-1600607686527-6fb886090705?q=80&w=2000&auto=format&fit=crop"
    verbose_name = "Approach Image (URL)"

@global_preferences_registry.register
class AboutApproachImageFile(FilePreference):
    section = about
    name = "approach_image_file"
    default = None
    verbose_name = "Approach Image (Upload)"

# Section: Home Page
home = Section('home')

# 1. Hero Image
@global_preferences_registry.register
class HomeHeroImage(StringPreference):
    section = home
    name = "hero_image"
    default = "https://images.unsplash.com/photo-1540518614846-7eded433c457?q=80&w=2057&auto=format&fit=crop"
    verbose_name = "Hero Image (URL)"

@global_preferences_registry.register
class HomeHeroImageFile(FilePreference):
    section = home
    name = "hero_image_file"
    default = None
    verbose_name = "Hero Image (Upload)"

# 2. Stats / Why Choose Us Image
@global_preferences_registry.register
class HomeStatsImage(StringPreference):
    section = home
    name = "stats_image"
    default = "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?q=80&w=2076&auto=format&fit=crop"
    verbose_name = "Stats/Why Choose Us Image (URL)"

@global_preferences_registry.register
class HomeStatsImageFile(FilePreference):
    section = home
    name = "stats_image_file"
    default = None
    verbose_name = "Stats/Why Choose Us Image (Upload)"

# 3. Balcony Covering Image
@global_preferences_registry.register
class HomeBalconyImage(StringPreference):
    section = home
    name = "balcony_image"
    default = "https://images.unsplash.com/photo-1628744876497-eb30460be9f6?q=80&w=2070&auto=format&fit=crop"
    verbose_name = "Balcony Covering Image (URL)"

@global_preferences_registry.register
class HomeBalconyImageFile(FilePreference):
    section = home
    name = "balcony_image_file"
    default = None
    verbose_name = "Balcony Covering Image (Upload)"

# 4. Safety Jali Door Image
@global_preferences_registry.register
class HomeJaliImage(StringPreference):
    section = home
    name = "jali_image"
    default = "https://images.unsplash.com/photo-1595846519845-68e298c2edd8?q=80&w=1887&auto=format&fit=crop"
    verbose_name = "Safety Jali Door Image (URL)"

@global_preferences_registry.register
class HomeJaliImageFile(FilePreference):
    section = home
    name = "jali_image_file"
    default = None
    verbose_name = "Safety Jali Door Image (Upload)"

# 5. Profile Panels Image
@global_preferences_registry.register
class HomeProfileImage(StringPreference):
    section = home
    name = "profile_image"
    default = "https://images.unsplash.com/photo-1615873968403-89e068629265?q=80&w=1932&auto=format&fit=crop"
    verbose_name = "Profile Panels Image (URL)"

@global_preferences_registry.register
class HomeProfileImageFile(FilePreference):
    section = home
    name = "profile_image_file"
    default = None
    verbose_name = "Profile Panels Image (Upload)"

# 6. Glass Partition Image
@global_preferences_registry.register
class HomeGlassImage(StringPreference):
    section = home
    name = "glass_image"
    default = "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=2070&auto=format&fit=crop"
    verbose_name = "Glass Partition Image (URL)"

@global_preferences_registry.register
class HomeGlassImageFile(FilePreference):
    section = home
    name = "glass_image_file"
    default = None
    verbose_name = "Glass Partition Image (Upload)"
